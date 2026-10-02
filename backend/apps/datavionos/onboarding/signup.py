from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from secrets import token_hex
from typing import Any

from django.db import transaction
from django.utils.text import slugify

from apps.datavionos.onboarding.contracts import OrganizationOnboardingRequest
from apps.datavionos.onboarding.plan_catalog import (
    plan_is_eligible_for_onboarding,
    validate_organization_profile,
)
from apps.datavionos.onboarding.registration import (
    OrganizationRegistrationOrchestrator,
)
from apps.platform.accounts.constants import OTPChannel, OTPPurpose
from apps.platform.accounts.models import User
from apps.platform.accounts.services import (
    AuthenticationService,
    OTPService,
    UserService,
)
from apps.platform.saas_billing.models import Plan
from apps.platform.tenancy.constants import TenantType
from apps.platform.tenancy.models import Tenant
from apps.platform.tenancy.services import TenantService


class SelfServiceSignupError(ValueError):
    pass


class SelfServicePaymentRequiredError(SelfServiceSignupError):
    pass


class SelfServiceEmailConflictError(SelfServiceSignupError):
    pass


@dataclass(frozen=True, slots=True)
class SelfServiceSignupResult:
    user: User
    organization_result: Any
    payment_required_now: bool
    payment_required_after_trial: bool
    next_step: str = "verify_email"

    def as_dict(self) -> dict[str, Any]:
        payload = self.organization_result.as_dict()
        return {
            "signup": {
                "status": "PENDING_EMAIL_VERIFICATION",
                "next_step": self.next_step,
                "verification_required": True,
            },
            "account": {
                "user_id": str(self.user.pk),
                "email": self.user.email,
                "email_verified": bool(self.user.is_verified),
            },
            "organization": payload.get("organization", {}),
            "subscription": payload.get("subscription", {}),
            "modules": payload.get("modules", []),
            "features": payload.get("features", []),
            "workspace": payload.get("workspace", "organization"),
            "payment": {
                "required_now": self.payment_required_now,
                "required_after_trial": self.payment_required_after_trial,
            },
        }


class SelfServiceSignupService:
    _TENANT_TYPE_MAP = {
        "hospital": TenantType.HOSPITAL,
        "government_hospital": TenantType.HOSPITAL,
        "laboratory": TenantType.LABORATORY,
        "diagnostic_center": TenantType.LABORATORY,
        "radiology_center": TenantType.LABORATORY,
        "imaging_center": TenantType.LABORATORY,
        "pathology_lab": TenantType.LABORATORY,
        "blood_bank": TenantType.LABORATORY,
        "retail_pharmacy": TenantType.PHARMACY,
        "hospital_pharmacy": TenantType.PHARMACY,
        "online_pharmacy": TenantType.PHARMACY,
        "wholesale_pharmacy": TenantType.PHARMACY,
        "corporate": TenantType.ENTERPRISE,
        "occupational_health": TenantType.ENTERPRISE,
        "healthcare_network": TenantType.ENTERPRISE,
        "insurance_company": TenantType.ENTERPRISE,
        "tpa": TenantType.ENTERPRISE,
        "medical_college": TenantType.ENTERPRISE,
        "medical_university": TenantType.ENTERPRISE,
        "research_institute": TenantType.ENTERPRISE,
        "clinical_trial_center": TenantType.ENTERPRISE,
        "public_health_center": TenantType.ENTERPRISE,
        "ngo": TenantType.ENTERPRISE,
        "ambulance_service": TenantType.CLINIC,
        "trauma_center": TenantType.CLINIC,
        "emergency_center": TenantType.CLINIC,
    }

    @classmethod
    def tenant_type_for_organization_type(
        cls,
        organization_type: str,
    ) -> str:
        normalized = str(organization_type or "").strip().lower()
        return cls._TENANT_TYPE_MAP.get(
            normalized,
            TenantType.CLINIC,
        )

    @staticmethod
    def unique_tenant_slug(name: str) -> str:
        base = slugify(name)[:80].strip("-")
        if not base:
            base = f"tenant-{token_hex(5)}"

        if not Tenant.objects.filter(slug=base).exists():
            return base

        for _ in range(25):
            candidate = f"{base[:70].rstrip('-')}-{token_hex(5)}"
            if not Tenant.objects.filter(slug=candidate).exists():
                return candidate

        raise SelfServiceSignupError("Unable to allocate a unique tenant identifier.")

    @staticmethod
    def payment_requirements(plan: Plan) -> tuple[bool, bool]:
        """Return upfront payment requirements for public self-service signup.

        A trial period is a subscription lifecycle feature, not authorization
        to provision a priced plan without payment. Public onboarding may
        automatically provision only zero-priced plans.
        """
        price = Decimal(str(plan.price or 0))
        paid = price > 0
        return paid, False

    @classmethod
    def resolve_plan(
        cls,
        *,
        category: str,
        organization_type: str,
        size: str,
        plan_id: Any | None = None,
        plan_code: str | None = None,
    ) -> Plan | None:
        queryset = Plan.objects.filter(
            is_active=True,
            is_public=True,
        )

        if plan_id is not None:
            queryset = queryset.filter(pk=plan_id)
        elif plan_code:
            queryset = queryset.filter(code=str(plan_code).strip())

        for plan in queryset.order_by("display_order", "price", "name"):
            if plan_is_eligible_for_onboarding(
                plan,
                category=category,
                organization_type=organization_type,
                size=size,
            ):
                return plan

        return None

    @classmethod
    def preflight(
        cls,
        *,
        organization_data: Mapping[str, Any],
        plan_id: Any | None = None,
        plan_code: str | None = None,
    ) -> dict[str, Any]:
        category, organization_type, size = validate_organization_profile(
            organization_data
        )

        plan = cls.resolve_plan(
            category=category,
            organization_type=organization_type,
            size=size,
            plan_id=plan_id,
            plan_code=plan_code,
        )

        if plan is None:
            return {
                "eligible": False,
                "category": category,
                "organization_type": organization_type,
                "size": size,
                "plan": None,
                "payment_required_now": False,
                "payment_required_after_trial": False,
                "next_step": "select_plan",
                "errors": [
                    "No active public SaaS plan is eligible for the selected organization profile."
                ],
            }

        payment_now, payment_after_trial = cls.payment_requirements(plan)
        errors = []

        if payment_now:
            errors.append(
                "This paid plan requires payment before an organization workspace can be created."
            )

        return {
            "eligible": not errors,
            "category": category,
            "organization_type": organization_type,
            "size": size,
            "plan": {
                "id": str(plan.pk),
                "code": plan.code,
                "name": plan.name,
                "price": str(plan.price),
                "currency": plan.currency,
                "billing_cycle": plan.billing_cycle,
                "trial_days": plan.trial_days,
            },
            "payment_required_now": payment_now,
            "payment_required_after_trial": payment_after_trial,
            "next_step": "payment" if payment_now else "register",
            "errors": errors,
        }

    @classmethod
    @transaction.atomic
    def signup(
        cls,
        *,
        account_data: Mapping[str, Any],
        organization_data: Mapping[str, Any],
        plan_id: Any | None = None,
        plan_code: str | None = None,
        ip_address: str | None = None,
        user_agent: str = "",
    ) -> SelfServiceSignupResult:
        email = str(account_data.get("email") or "").strip().lower()

        if User.objects.filter(email=email).exists():
            raise SelfServiceEmailConflictError(
                "An account with this email is already registered. Use login or password recovery instead."
            )

        category, organization_type, size = validate_organization_profile(
            organization_data
        )

        plan = cls.resolve_plan(
            category=category,
            organization_type=organization_type,
            size=size,
            plan_id=plan_id,
            plan_code=plan_code,
        )

        if plan is None:
            raise SelfServiceSignupError(
                "No active public SaaS plan is eligible for the selected organization profile."
            )

        payment_now, payment_after_trial = cls.payment_requirements(plan)

        if payment_now:
            raise SelfServicePaymentRequiredError(
                "The selected paid plan requires payment before signup. No organization or trial subscription was created."
            )

        organization_name = str(organization_data.get("name") or "").strip()

        if not organization_name:
            raise SelfServiceSignupError("organization name is required.")

        tenant = TenantService.create_tenant(
            name=organization_name,
            slug=cls.unique_tenant_slug(organization_name),
            tenant_type=cls.tenant_type_for_organization_type(organization_type),
            owner=None,
        )

        user = UserService.create(
            email=email,
            password=account_data.get("password"),
            first_name=str(account_data.get("first_name") or "").strip(),
            last_name=str(account_data.get("last_name") or "").strip(),
            phone=str(account_data.get("phone") or "").strip(),
            is_internal_user=False,
        )

        from apps.platform.tenancy.services.membership import (
            TenantMembershipService,
        )

        TenantMembershipService.create_membership(
            tenant=tenant,
            user=user,
            is_owner=True,
        )

        # Make the newly created tenant the user's active runtime context so
        # the first authenticated bootstrap sees its subscription and modules.
        from apps.platform.tenancy.models import UserTenantPreference

        UserTenantPreference.objects.update_or_create(
            user=user,
            defaults={"tenant": tenant},
        )

        organization_payload = {
            **dict(organization_data),
            "category": category,
            "organization_type": organization_type,
            "size": size,
        }

        organization_result = OrganizationRegistrationOrchestrator.register(
            request=OrganizationOnboardingRequest(
                tenant=tenant,
                organization_data=organization_payload,
                plan_id=plan.pk,
                plan_code=plan.code,
                owner_user=user,
                metadata={
                    "signup_source": "self_service",
                },
            )
        )

        otp_result = OTPService.create(
            user=user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            recipient=user.email,
            channel=OTPChannel.EMAIL,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        transaction.on_commit(
            lambda: AuthenticationService._send_verification_otp(
                user=user,
                code=otp_result.code,
            )
        )

        return SelfServiceSignupResult(
            user=user,
            organization_result=organization_result,
            payment_required_now=payment_now,
            payment_required_after_trial=payment_after_trial,
        )


__all__ = [
    "SelfServiceEmailConflictError",
    "SelfServicePaymentRequiredError",
    "SelfServiceSignupError",
    "SelfServiceSignupResult",
    "SelfServiceSignupService",
]

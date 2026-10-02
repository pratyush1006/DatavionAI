from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from django.db import transaction
from django.utils.text import slugify

from apps.datavionos.onboarding.contracts import (
    OrganizationOnboardingRequest,
    OrganizationOnboardingResult,
)
from apps.datavionos.onboarding.plan_catalog import (
    plan_is_eligible_for_onboarding,
    validate_organization_profile,
)
from apps.datavionos.onboarding.provisioning import (
    OrganizationOnboardingProvisioner,
)
from apps.platform.organizations.models import (
    Organization,
    OrganizationProfile,
    OrganizationSettings,
)
from apps.platform.organizations.services.organization_branding import (
    create_branding,
)
from apps.platform.saas_billing.models import Plan


class OrganizationRegistrationError(ValueError):
    """Expected registration workflow error."""


@dataclass(frozen=True, slots=True)
class OrganizationRegistrationPreflight:
    eligible: bool
    organization_type: str
    category: str
    size: str
    plan: dict[str, Any] | None
    payment_required: bool
    verification_required: bool
    next_step: str
    errors: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class OrganizationRegistrationResult:
    onboarding: OrganizationOnboardingResult
    next_step: str
    verification_required: bool
    payment_required: bool
    idempotent_replay: bool = False

    def as_dict(self) -> dict[str, Any]:
        payload = self.onboarding.as_dict()
        payload["registration"] = {
            "status": "completed",
            "next_step": self.next_step,
            "verification_required": self.verification_required,
            "payment_required": self.payment_required,
            "idempotent_replay": self.idempotent_replay,
        }
        return payload


class OrganizationRegistrationOrchestrator:
    """Canonical backend-owned organization registration orchestrator."""

    DEFAULT_NEXT_STEP = "bootstrap"

    @staticmethod
    def _text(value: Any) -> str:
        return str(value or "").strip()

    @staticmethod
    def _payment_required(plan: Plan) -> bool:
        # A trial period does not waive payment for a priced public plan.
        # This guard is duplicated at the orchestration layer so internal
        # callers cannot bypass the self-service signup policy.
        return Decimal(str(getattr(plan, "price", 0) or 0)) > 0

    @classmethod
    def _resolve_plan(
        cls,
        *,
        organization_type: str,
        category: str,
        size: str,
        plan_id: Any | None,
        plan_code: str | None,
    ) -> Plan | None:
        queryset = Plan.objects.filter(
            is_active=True,
            is_public=True,
        )

        if plan_id is not None:
            candidates = queryset.filter(pk=plan_id)
        elif plan_code:
            candidates = queryset.filter(
                code=str(plan_code).strip(),
            )
        else:
            candidates = queryset

        for plan in candidates.order_by(
            "display_order",
            "price",
            "name",
        ):
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
    ) -> OrganizationRegistrationPreflight:
        category, organization_type, size = validate_organization_profile(
            organization_data
        )

        plan = cls._resolve_plan(
            organization_type=organization_type,
            category=category,
            size=size,
            plan_id=plan_id,
            plan_code=plan_code,
        )

        errors: list[str] = []

        if plan is None:
            errors.append(
                "No active public SaaS plan is eligible for the selected organization profile."
            )

        payment_required = bool(plan and cls._payment_required(plan))

        plan_payload = None

        if plan is not None:
            plan_payload = {
                "id": str(plan.pk),
                "code": plan.code,
                "name": plan.name,
                "description": plan.description,
                "plan_type": plan.plan_type,
                "healthcare_segment": plan.healthcare_segment,
                "price": str(plan.price),
                "currency": plan.currency,
                "billing_cycle": plan.billing_cycle,
                "trial_days": plan.trial_days,
                "modules": plan.modules,
                "features": plan.features,
                "limits": plan.limits,
            }

        return OrganizationRegistrationPreflight(
            eligible=not errors,
            organization_type=organization_type,
            category=category,
            size=size,
            plan=plan_payload,
            payment_required=payment_required,
            verification_required=True,
            next_step=("payment" if payment_required else "bootstrap"),
            errors=tuple(errors),
        )

    @staticmethod
    def _ensure_defaults(
        organization: Organization,
    ) -> None:
        OrganizationProfile.objects.get_or_create(
            organization=organization,
            defaults={
                "industry": "healthcare",
                "facility_type": organization.organization_type,
                "description": organization.description or "",
                "license_number": organization.license_number or "",
                "metadata": {},
            },
        )

        OrganizationSettings.objects.get_or_create(
            organization=organization,
            defaults={
                "timezone": organization.timezone or "Asia/Kolkata",
                "currency": "INR",
                "default_dashboard": "main",
            },
        )

        if not hasattr(
            organization,
            "branding",
        ):
            create_branding(
                validated_data={
                    "organization": organization,
                },
            )

    @classmethod
    @transaction.atomic
    def register(
        cls,
        *,
        request: OrganizationOnboardingRequest,
    ) -> OrganizationRegistrationResult:
        if request.tenant is None:
            raise OrganizationRegistrationError(
                "tenant is required.",
            )

        category, organization_type, size = validate_organization_profile(
            request.organization_data
        )

        plan = cls._resolve_plan(
            organization_type=organization_type,
            category=category,
            size=size,
            plan_id=request.plan_id,
            plan_code=request.plan_code,
        )

        if plan is None:
            raise OrganizationRegistrationError(
                "No active public SaaS plan is eligible for the selected organization profile."
            )

        if cls._payment_required(plan):
            raise OrganizationRegistrationError(
                "The selected paid plan requires a completed payment before an organization or subscription can be provisioned."
            )

        data = dict(request.organization_data)
        data["category"] = category
        data["organization_type"] = organization_type
        data["size"] = size

        name = cls._text(
            data.get("name"),
        )

        if not name:
            raise OrganizationRegistrationError(
                "organization name is required.",
            )

        code = (
            cls._text(data.get("code")).upper()
            or slugify(name).replace("-", "_")[:20].upper()
        )

        slug = cls._text(data.get("slug")) or slugify(name)[:100]

        existing = Organization.objects.filter(
            tenant=request.tenant,
            code=code,
        ).first()

        replay = existing is not None

        result = OrganizationOnboardingProvisioner.provision(
            OrganizationOnboardingRequest(
                tenant=request.tenant,
                organization_data={
                    **data,
                    "code": code,
                    "slug": slug,
                },
                plan_id=plan.pk,
                plan_code=plan.code,
                owner_user=request.owner_user,
                metadata=request.metadata,
            )
        )

        cls._ensure_defaults(
            result.organization,
        )

        payment_required = cls._payment_required(
            result.subscription.plan,
        )

        return OrganizationRegistrationResult(
            onboarding=result,
            next_step=("payment" if payment_required else cls.DEFAULT_NEXT_STEP),
            verification_required=True,
            payment_required=payment_required,
            idempotent_replay=replay,
        )


__all__ = [
    "OrganizationRegistrationError",
    "OrganizationRegistrationOrchestrator",
    "OrganizationRegistrationPreflight",
    "OrganizationRegistrationResult",
]

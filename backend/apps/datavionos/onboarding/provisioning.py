from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from apps.datavionos.onboarding.contracts import (
    OrganizationOnboardingRequest,
    OrganizationOnboardingResult,
)
from apps.datavionos.onboarding.plan_catalog import (
    OrganizationOnboardingValidationError,
    plan_is_eligible_for_onboarding,
    validate_organization_profile,
)
from apps.datavionos.onboarding.registration_billing import RegistrationBillingService
from apps.platform.organizations.models import (
    Organization,
    OrganizationFeature,
    OrganizationModule,
)
from apps.platform.organizations.services.organization import activate_organization
from apps.platform.organizations.services.organization_feature import create_feature
from apps.platform.organizations.services.organization_module import create_module
from apps.platform.rbac.models import OrganizationRole, Role
from apps.platform.saas_billing.models import Plan, Subscription
from apps.platform.saas_billing.services.subscription_service import (
    SubscriptionService,
)


class OrganizationOnboardingError(ValueError):
    """Expected onboarding validation/provisioning error."""


class OrganizationPlanMismatchError(OrganizationOnboardingError):
    """Selected plan is incompatible with the organization type."""


class OrganizationOnboardingProvisioner:
    """Canonical application orchestration boundary for SaaS onboarding."""

    DEFAULT_WORKSPACE = "organization"

    @staticmethod
    def _text(value: Any) -> str:
        return str(value or "").strip()

    @classmethod
    def _organization_type(cls, data: Mapping[str, Any]) -> str:
        value = cls._text(data.get("organization_type"))
        if not value:
            raise OrganizationOnboardingError("organization_type is required.")
        return value.lower()

    @classmethod
    def _resolve_plan(
        cls,
        request: OrganizationOnboardingRequest,
        organization_type: str,
    ) -> Plan:
        category = cls._text(request.organization_data.get("category")).lower()
        size = cls._text(request.organization_data.get("size")).lower()

        try:
            validate_organization_profile(
                request.organization_data,
            )
        except OrganizationOnboardingValidationError:
            raise

        manager = Plan.objects.filter(
            is_active=True,
            is_public=True,
        )

        if request.plan_id is not None:
            candidates = manager.filter(
                pk=request.plan_id,
            )
        elif request.plan_code:
            candidates = manager.filter(
                code=cls._text(request.plan_code),
            )
        else:
            candidates = manager

        for candidate in candidates.order_by(
            "display_order",
            "price",
            "name",
        ):
            if plan_is_eligible_for_onboarding(
                candidate,
                category=category,
                organization_type=organization_type,
                size=size,
            ):
                return candidate

        if request.plan_id is not None or request.plan_code:
            raise OrganizationPlanMismatchError(
                "Selected SaaS plan is not eligible for the organization "
                "category, type, and size."
            )

        raise OrganizationOnboardingError(
            "No active public SaaS plan is eligible for the selected "
            "organization profile."
        )

    @staticmethod
    def _normalize_mapping(value: Any) -> dict[str, bool]:
        if not isinstance(value, Mapping):
            return {}

        return {
            str(key).strip(): enabled
            for key, enabled in value.items()
            if str(key).strip() and isinstance(enabled, bool)
        }

    @classmethod
    def _provision_modules(
        cls,
        organization: Organization,
        plan: Plan,
    ) -> tuple[str, ...]:
        entitled = cls._normalize_mapping(getattr(plan, "modules", {}))
        now = timezone.now()
        enabled: list[str] = []

        for module_code, is_entitled in entitled.items():
            if not is_entitled:
                continue

            assignment = OrganizationModule.objects.filter(
                organization=organization,
                module_code=module_code,
            ).first()

            if assignment is None:
                create_module(
                    validated_data={
                        "organization": organization,
                        "module_code": module_code,
                        "status": OrganizationModule.Status.ENABLED,
                        "settings": {},
                        "enabled_at": now,
                        "disabled_at": None,
                    }
                )
            elif assignment.status != OrganizationModule.Status.ENABLED:
                assignment.status = OrganizationModule.Status.ENABLED
                assignment.enabled_at = assignment.enabled_at or now
                assignment.disabled_at = None
                assignment.save(
                    update_fields=[
                        "status",
                        "enabled_at",
                        "disabled_at",
                        "updated_at",
                    ],
                )

            enabled.append(module_code)

        return tuple(sorted(set(enabled)))

    @classmethod
    def _provision_features(
        cls,
        organization: Organization,
        plan: Plan,
    ) -> tuple[str, ...]:
        entitled = cls._normalize_mapping(getattr(plan, "features", {}))
        now = timezone.now()
        enabled: list[str] = []

        for feature_code, is_entitled in entitled.items():
            if not is_entitled:
                continue

            assignment = OrganizationFeature.objects.filter(
                organization=organization,
                feature_code=feature_code,
            ).first()

            if assignment is None:
                create_feature(
                    validated_data={
                        "organization": organization,
                        "feature_code": feature_code,
                        "status": OrganizationFeature.FeatureStatus.ENABLED,
                        "settings": {},
                        "enabled_at": now,
                        "disabled_at": None,
                    }
                )
            elif assignment.status != OrganizationFeature.FeatureStatus.ENABLED:
                assignment.status = OrganizationFeature.FeatureStatus.ENABLED
                assignment.enabled_at = assignment.enabled_at or now
                assignment.disabled_at = None
                assignment.save(
                    update_fields=[
                        "status",
                        "enabled_at",
                        "disabled_at",
                        "updated_at",
                    ],
                )

            enabled.append(feature_code)

        return tuple(sorted(set(enabled)))

    @classmethod
    def _assign_organization_admin(
        cls,
        organization: Organization,
        owner_user: Any | None,
    ) -> bool:
        if owner_user is None:
            return False

        role = Role.objects.filter(
            code="organization_admin",
            is_active=True,
        ).first()

        if role is None:
            raise OrganizationOnboardingError(
                "Required RBAC role 'organization_admin' is not configured."
            )

        OrganizationRole.objects.update_or_create(
            organization=organization,
            user=owner_user,
            role=role,
            defaults={
                "is_primary": True,
                "is_active": True,
            },
        )
        return True

    @classmethod
    @transaction.atomic
    def provision(
        cls,
        request: OrganizationOnboardingRequest,
    ) -> OrganizationOnboardingResult:
        if request.tenant is None:
            raise OrganizationOnboardingError("tenant is required.")

        data = dict(request.organization_data)
        organization_type = cls._organization_type(data)
        plan = cls._resolve_plan(request, organization_type)

        name = cls._text(data.get("name"))
        if not name:
            raise OrganizationOnboardingError("organization name is required.")

        code = (
            cls._text(data.get("code")).upper()
            or slugify(name).replace("-", "_")[:20].upper()
        )
        slug = cls._text(data.get("slug")) or slugify(name)[:100]

        organization = Organization.objects.filter(
            tenant=request.tenant,
            code=code,
        ).first()
        created_organization = organization is None

        if organization is None:
            allowed_fields = {
                "name",
                "display_name",
                "code",
                "slug",
                "category",
                "organization_type",
                "size",
                "email",
                "support_email",
                "phone",
                "website",
                "address",
                "city",
                "state",
                "country",
                "country_ref",
                "region_ref",
                "city_ref",
                "postal_code",
                "timezone",
                "registration_number",
                "tax_number",
                "license_number",
                "accreditation",
                "description",
                "is_demo",
            }
            create_data = {
                key: value
                for key, value in data.items()
                if key in allowed_fields and value is not None
            }
            create_data.update(
                {
                    "tenant": request.tenant,
                    "name": name,
                    "display_name": (cls._text(data.get("display_name")) or name),
                    "code": code,
                    "slug": slug,
                    "organization_type": organization_type,
                }
            )
            organization = Organization.objects.create(**create_data)

            # DatavionOS canonical registration lifecycle.
            # Newly registered organizations are immediately
            # operationally active. Lifecycle status is never
            # accepted from the registration UI.
            organization = activate_organization(
                instance=organization,
            )

        subscription = (
            Subscription.objects.filter(organization=organization)
            .select_related("plan")
            .first()
        )
        created_subscription = subscription is None

        if subscription is None:
            subscription = SubscriptionService.create_trial_subscription(
                organization=organization,
                plan=plan,
            )
        elif subscription.plan_id != plan.pk:
            raise OrganizationOnboardingError(
                "Organization already has a different subscription plan. "
                "Use subscription plan-management workflows."
            )

        registration_billing = RegistrationBillingService.create_registration_invoice(
            subscription=subscription,
        )

        modules = cls._provision_modules(
            organization,
            subscription.plan,
        )
        features = cls._provision_features(
            organization,
            subscription.plan,
        )
        admin_assigned = cls._assign_organization_admin(
            organization,
            request.owner_user,
        )

        return OrganizationOnboardingResult(
            organization=organization,
            subscription=subscription,
            modules=modules,
            features=features,
            workspace=cls.DEFAULT_WORKSPACE,
            created_organization=created_organization,
            created_subscription=created_subscription,
            registration_billing=(registration_billing.as_dict()),
            organization_admin_assigned=admin_assigned,
        )


provision_organization_onboarding = OrganizationOnboardingProvisioner.provision

__all__ = [
    "OrganizationOnboardingError",
    "OrganizationOnboardingProvisioner",
    "OrganizationPlanMismatchError",
    "provision_organization_onboarding",
]

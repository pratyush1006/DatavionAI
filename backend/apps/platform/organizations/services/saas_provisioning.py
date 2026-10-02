from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.db import transaction

from apps.platform.organizations.models import Organization
from apps.platform.saas_billing.models import Plan, Subscription
from apps.platform.saas_billing.services.subscription_service import SubscriptionService


class OrganizationProvisioningError(ValueError):
    """Raised when organization type and SaaS plan cannot be provisioned safely."""


@dataclass(frozen=True, slots=True)
class OrganizationSaaSProvisioningResult:
    """Immutable result of organization-to-plan SaaS provisioning."""

    organization_id: str
    organization_type: str
    healthcare_segment: str
    plan_code: str
    subscription_status: str
    modules: dict[str, bool]
    features: dict[str, bool]


# Organization classification is the customer-facing vocabulary; Plan uses
# HealthcareSegment. Keep this mapping here as an onboarding translation
# boundary instead of duplicating segment logic throughout registration.
ORGANIZATION_TYPE_TO_SEGMENT: dict[str, str] = {
    "HOSPITAL": "HOSPITAL",
    "CLINIC": "CLINIC",
    "PHARMACY": "PHARMACY",
    "MEDICAL_STORE": "PHARMACY",
    "LABORATORY": "LABORATORY",
    "DIAGNOSTIC_LABORATORY": "LABORATORY",
    "IMAGING": "IMAGING",
    "IMAGING_CENTER": "IMAGING",
    "DENTAL": "DENTAL",
    "DENTAL_CLINIC": "DENTAL",
    "PHYSIOTHERAPY": "PHYSIOTHERAPY",
    "PHYSIOTHERAPY_CENTER": "PHYSIOTHERAPY",
    "NURSING_HOME": "NURSING_HOME",
    "ENTERPRISE": "ENTERPRISE",
    "HEALTHCARE_ENTERPRISE": "ENTERPRISE",
}


def _normalize_classification(value: Any) -> str:
    """Normalize signup organization type without changing persisted data."""

    if not isinstance(value, str):
        return ""
    return value.strip().upper().replace("-", "_").replace(" ", "_")


def resolve_healthcare_segment(organization_type: Any) -> str:
    """Translate organization type into the canonical Plan segment."""

    normalized = _normalize_classification(organization_type)
    segment = ORGANIZATION_TYPE_TO_SEGMENT.get(normalized)
    if not segment:
        raise OrganizationProvisioningError(
            f"Unsupported organization type for SaaS provisioning: {organization_type!r}"
        )
    return segment


def resolve_signup_plan(
    *, organization_type: Any, plan_code: str | None = None
) -> Plan:
    """Resolve a plan whose healthcare segment matches the organization type."""

    segment = resolve_healthcare_segment(organization_type)
    queryset = Plan.objects.filter(
        is_active=True,
        healthcare_segment=segment,
    )

    if plan_code:
        normalized_code = plan_code.strip()
        if not normalized_code:
            raise OrganizationProvisioningError(
                "plan_code cannot be blank when supplied"
            )
        plan = queryset.filter(code=normalized_code).first()
        if plan is None:
            raise OrganizationProvisioningError(
                "Requested SaaS plan is not active or does not match "
                f"organization type {organization_type!r}."
            )
        return plan

    plan = (
        queryset.filter(is_public=True)
        .order_by(
            "-is_default",
            "display_order",
            "price",
            "code",
        )
        .first()
    )
    if plan is None:
        # A non-public default is still a valid platform-configured fallback.
        plan = queryset.order_by(
            "-is_default",
            "display_order",
            "price",
            "code",
        ).first()

    if plan is None:
        raise OrganizationProvisioningError(
            f"No active SaaS plan is configured for healthcare segment {segment!r}."
        )

    return plan


@transaction.atomic
def provision_organization_saas(
    *,
    organization: Organization,
    plan_code: str | None = None,
) -> OrganizationSaaSProvisioningResult:
    """Provision the organization's initial SaaS subscription deterministically.

    The subscription snapshot is the SaaS entitlement authority. This service
    deliberately does not create dashboard state or grant modules outside the
    selected plan. OrganizationModule remains a customer ON/OFF override layer.
    """

    if organization is None:
        raise OrganizationProvisioningError("organization is required")

    segment = resolve_healthcare_segment(organization.organization_type)
    plan = resolve_signup_plan(
        organization_type=organization.organization_type,
        plan_code=plan_code,
    )

    if plan.healthcare_segment != segment:
        raise OrganizationProvisioningError(
            "SaaS plan healthcare segment does not match organization type."
        )

    existing = (
        Subscription.objects.select_related("plan")
        .filter(organization=organization)
        .first()
    )

    if existing is not None:
        if existing.plan.healthcare_segment != segment:
            raise OrganizationProvisioningError(
                "Existing subscription violates organization-type/plan segment invariant."
            )
        if plan_code and existing.plan.code != plan.code:
            raise OrganizationProvisioningError(
                "Organization already has a different subscription; plan changes "
                "must use the subscription plan-management workflow."
            )
        subscription = existing
    else:
        subscription = SubscriptionService.create_trial_subscription(
            organization=organization,
            plan=plan,
        )

    snapshot = (
        subscription.feature_snapshot
        if isinstance(subscription.feature_snapshot, dict)
        else {}
    )
    modules_raw = snapshot.get("modules", {})
    features_raw = snapshot.get("features", {})
    modules = {
        str(k): True for k, v in modules_raw.items() if isinstance(k, str) and v is True
    }
    features = {
        str(k): True
        for k, v in features_raw.items()
        if isinstance(k, str) and v is True
    }

    return OrganizationSaaSProvisioningResult(
        organization_id=str(organization.pk),
        organization_type=_normalize_classification(organization.organization_type),
        healthcare_segment=segment,
        plan_code=subscription.plan.code,
        subscription_status=subscription.status,
        modules=modules,
        features=features,
    )


__all__ = (
    "ORGANIZATION_TYPE_TO_SEGMENT",
    "OrganizationProvisioningError",
    "OrganizationSaaSProvisioningResult",
    "provision_organization_saas",
    "resolve_healthcare_segment",
    "resolve_signup_plan",
)

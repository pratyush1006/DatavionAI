from __future__ import annotations

from typing import Any

from apps.datavionos.control_plane.contracts import OrganizationControlPlaneSnapshot
from apps.platform.organizations.models import OrganizationFeature, OrganizationModule
from apps.platform.organizations.policies.organization_policy import OrganizationPolicy
from apps.platform.saas_billing.models import Subscription


class OrganizationControlPlaneService:
    """Compose organization administration state without owning SaaS rules."""

    def __init__(self, *, policy: OrganizationPolicy | None = None) -> None:
        self._policy = policy or OrganizationPolicy()

    def resolve(
        self, *, user: Any, organization: Any
    ) -> OrganizationControlPlaneSnapshot:
        modules = OrganizationModule.objects.filter(organization=organization).order_by(
            "module_code"
        )
        features = OrganizationFeature.objects.filter(
            organization=organization
        ).order_by("feature_code")
        subscription = (
            Subscription.objects.select_related("plan")
            .filter(organization=organization)
            .first()
        )
        subscription_data = None
        if subscription is not None:
            plan = getattr(subscription, "plan", None)
            subscription_data = {
                "id": str(subscription.pk),
                "status": str(subscription.status),
                "plan": {
                    "id": str(plan.pk) if plan is not None else None,
                    "name": getattr(plan, "name", None),
                    "code": getattr(plan, "code", None),
                    "healthcare_segment": getattr(plan, "healthcare_segment", None),
                },
                "starts_at": (
                    getattr(subscription, "starts_at", None).isoformat()
                    if getattr(subscription, "starts_at", None)
                    else None
                ),
                "ends_at": (
                    getattr(subscription, "ends_at", None).isoformat()
                    if getattr(subscription, "ends_at", None)
                    else None
                ),
            }

        return OrganizationControlPlaneSnapshot(
            organization={
                "id": str(organization.pk),
                "name": organization.name,
                "display_name": organization.display_name,
                "code": organization.code,
                "organization_type": organization.organization_type,
                "status": organization.status,
                "is_active": organization.is_active,
            },
            subscription=subscription_data,
            modules=[
                {
                    "id": str(item.pk),
                    "module_code": item.module_code,
                    "status": item.status,
                    "settings": item.settings,
                    "enabled_at": (
                        item.enabled_at.isoformat() if item.enabled_at else None
                    ),
                    "disabled_at": (
                        item.disabled_at.isoformat() if item.disabled_at else None
                    ),
                }
                for item in modules
            ],
            features=[
                {
                    "id": str(item.pk),
                    "feature_code": item.feature_code,
                    "feature_name": getattr(item, "feature_name", None),
                    "status": item.status,
                    "configuration": getattr(
                        item, "configuration", getattr(item, "settings", {})
                    ),
                    "enabled_at": (
                        item.enabled_at.isoformat() if item.enabled_at else None
                    ),
                    "disabled_at": (
                        item.disabled_at.isoformat() if item.disabled_at else None
                    ),
                }
                for item in features
            ],
            can_manage_modules=self._policy.can_manage_modules(
                actor=user, organization=organization
            ),
            can_manage_features=self._policy.can_manage_features(
                actor=user, organization=organization
            ),
        )

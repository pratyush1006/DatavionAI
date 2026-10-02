from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class OrganizationOnboardingRequest:
    """Validated onboarding input entering the application control plane."""

    tenant: Any
    organization_data: Mapping[str, Any]
    plan_id: Any | None = None
    plan_code: str | None = None
    owner_user: Any | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class OrganizationOnboardingResult:
    """Stable application result returned after successful provisioning."""

    organization: Any
    subscription: Any
    modules: tuple[str, ...]
    features: tuple[str, ...]
    workspace: str
    created_organization: bool
    created_subscription: bool
    organization_admin_assigned: bool = False
    registration_billing: dict[str, Any] = field(
        default_factory=dict,
    )

    def as_dict(self) -> dict[str, Any]:
        organization = self.organization
        subscription = self.subscription
        plan = getattr(subscription, "plan", None)

        return {
            "organization": {
                "id": str(getattr(organization, "pk", "")),
                "name": getattr(organization, "name", ""),
                "display_name": getattr(organization, "display_name", ""),
                "code": getattr(organization, "code", ""),
                "slug": getattr(organization, "slug", ""),
                "category": getattr(organization, "category", ""),
                "organization_type": getattr(
                    organization,
                    "organization_type",
                    "",
                ),
                "size": getattr(organization, "size", ""),
            },
            "subscription": {
                "id": str(getattr(subscription, "pk", "")),
                "status": getattr(subscription, "status", ""),
                "plan": {
                    "id": str(getattr(plan, "pk", "")),
                    "code": getattr(plan, "code", ""),
                    "name": getattr(plan, "name", ""),
                    "healthcare_segment": getattr(
                        plan,
                        "healthcare_segment",
                        "",
                    ),
                    "billing_cycle": getattr(
                        plan,
                        "billing_cycle",
                        "",
                    ),
                    "trial_days": getattr(
                        plan,
                        "trial_days",
                        0,
                    ),
                },
            },
            "modules": list(self.modules),
            "features": list(self.features),
            "workspace": self.workspace,
            "created_organization": self.created_organization,
            "created_subscription": self.created_subscription,
            "organization_admin_assigned": self.organization_admin_assigned,
            "registration_billing": self.registration_billing,
        }


__all__ = [
    "OrganizationOnboardingRequest",
    "OrganizationOnboardingResult",
]

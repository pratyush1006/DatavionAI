from __future__ import annotations

from apps.datavionos.onboarding.contracts import (
    OrganizationOnboardingRequest,
    OrganizationOnboardingResult,
)
from apps.datavionos.onboarding.provisioning import (
    provision_organization_onboarding,
)


class RegisterOrganizationWorkflow:
    """Application workflow for registration-to-provisioning."""

    def __init__(
        self,
        *,
        request: OrganizationOnboardingRequest,
    ) -> None:
        self.request = request

    def handle(self) -> OrganizationOnboardingResult:
        return provision_organization_onboarding(self.request)


__all__ = ["RegisterOrganizationWorkflow"]

"""
Organization workflow registration.

Registers organization workflows into the DatavionOS
core workflow registry.
"""

from __future__ import annotations

import logging

from apps.core.workflows import workflow_registry
from apps.platform.organizations.workflows import (
    OrganizationActivationWorkflow,
    OrganizationBrandingUpdateWorkflow,
    OrganizationCreationWorkflow,
    OrganizationDeactivationWorkflow,
    OrganizationDeletionWorkflow,
    OrganizationFeatureManagementWorkflow,
    OrganizationHierarchyManagementWorkflow,
    OrganizationModuleManagementWorkflow,
    OrganizationOffboardingWorkflow,
    OrganizationOnboardingWorkflow,
    OrganizationRestorationWorkflow,
    OrganizationSettingsUpdateWorkflow,
    OrganizationSuspensionWorkflow,
    OrganizationUpdateWorkflow,
    OrganizationVerificationWorkflow,
)

logger = logging.getLogger(__name__)


_registered = False


def register_organization_workflows() -> int:
    """
    Register organization workflows.

    Returns
    -------
    int
        Number of workflows registered.
    """

    global _registered

    if _registered:
        return 0

    workflows = {
        "organization.create": OrganizationCreationWorkflow,
        "organization.update": OrganizationUpdateWorkflow,
        "organization.activate": OrganizationActivationWorkflow,
        "organization.deactivate": OrganizationDeactivationWorkflow,
        "organization.suspend": OrganizationSuspensionWorkflow,
        "organization.restore": OrganizationRestorationWorkflow,
        "organization.verify": OrganizationVerificationWorkflow,
        "organization.delete": OrganizationDeletionWorkflow,
        "organization.branding.update": (OrganizationBrandingUpdateWorkflow),
        "organization.settings.update": (OrganizationSettingsUpdateWorkflow),
        "organization.feature.manage": (OrganizationFeatureManagementWorkflow),
        "organization.module.manage": (OrganizationModuleManagementWorkflow),
        "organization.hierarchy.manage": (OrganizationHierarchyManagementWorkflow),
        "organization.onboarding": (OrganizationOnboardingWorkflow),
        "organization.offboarding": (OrganizationOffboardingWorkflow),
    }

    registered_count = 0

    for name, workflow in workflows.items():
        if workflow_registry.is_registered(name):
            continue

        workflow_registry.register(
            name=name,
            workflow=workflow,
        )

        registered_count += 1

    _registered = True

    logger.info(
        "Organization workflows registered.",
        extra={
            "count": registered_count,
        },
    )

    return registered_count


__all__: tuple[str, ...] = ("register_organization_workflows",)

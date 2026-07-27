"""
Organization workflows.

Public workflow API for the Organizations bounded context.
"""

from __future__ import annotations

# ============================================================
# Organization Management Workflows
# ============================================================
from apps.platform.organizations.workflows.branding_update import (
    OrganizationBrandingUpdateWorkflow,
)
from apps.platform.organizations.workflows.feature_management import (
    OrganizationFeatureManagementWorkflow,
)
from apps.platform.organizations.workflows.hierarchy_management import (
    OrganizationHierarchyManagementWorkflow,
)
from apps.platform.organizations.workflows.module_management import (
    OrganizationModuleManagementWorkflow,
)

# ============================================================
# Organization Lifecycle Workflows
# ============================================================
from apps.platform.organizations.workflows.organization_activation import (
    OrganizationActivationWorkflow,
)
from apps.platform.organizations.workflows.organization_creation import (
    OrganizationCreationWorkflow,
)
from apps.platform.organizations.workflows.organization_deactivation import (
    OrganizationDeactivationWorkflow,
)
from apps.platform.organizations.workflows.organization_deletion import (
    OrganizationDeletionWorkflow,
)

# ============================================================
# Organization Onboarding Workflows
# ============================================================
from apps.platform.organizations.workflows.organization_offboarding import (
    OrganizationOffboardingWorkflow,
)
from apps.platform.organizations.workflows.organization_onboarding import (
    OrganizationOnboardingWorkflow,
)
from apps.platform.organizations.workflows.organization_restoration import (
    OrganizationRestorationWorkflow,
)
from apps.platform.organizations.workflows.organization_suspension import (
    OrganizationSuspensionWorkflow,
)
from apps.platform.organizations.workflows.organization_update import (
    OrganizationUpdateWorkflow,
)
from apps.platform.organizations.workflows.organization_verification import (
    OrganizationVerificationWorkflow,
)
from apps.platform.organizations.workflows.settings_update import (
    OrganizationSettingsUpdateWorkflow,
)

__all__: tuple[str, ...] = (
    "OrganizationActivationWorkflow",
    "OrganizationBrandingUpdateWorkflow",
    "OrganizationCreationWorkflow",
    "OrganizationDeactivationWorkflow",
    "OrganizationDeletionWorkflow",
    "OrganizationFeatureManagementWorkflow",
    "OrganizationHierarchyManagementWorkflow",
    "OrganizationModuleManagementWorkflow",
    "OrganizationOffboardingWorkflow",
    "OrganizationOnboardingWorkflow",
    "OrganizationRestorationWorkflow",
    "OrganizationSettingsUpdateWorkflow",
    "OrganizationSuspensionWorkflow",
    "OrganizationUpdateWorkflow",
    "OrganizationVerificationWorkflow",
)

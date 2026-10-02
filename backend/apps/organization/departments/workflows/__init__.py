"""
Department workflow exports.

Central export point for department
business workflows.
"""

from __future__ import annotations

from apps.organization.departments.workflows.department_activation import (
    DepartmentActivationWorkflow,
)
from apps.organization.departments.workflows.department_creation import (
    DepartmentCreationData,
    DepartmentCreationRequest,
    DepartmentCreationWorkflow,
)
from apps.organization.departments.workflows.department_deactivation import (
    DepartmentDeactivationWorkflow,
)
from apps.organization.departments.workflows.department_deletion import (
    DepartmentDeletionData,
    DepartmentDeletionRequest,
    DepartmentDeletionWorkflow,
)
from apps.organization.departments.workflows.department_hierarchy_management import (
    DepartmentHierarchyManagementWorkflow,
)
from apps.organization.departments.workflows.department_member_assignment import (
    DepartmentMemberAssignmentWorkflow,
)
from apps.organization.departments.workflows.department_role_management import (
    DepartmentRoleManagementWorkflow,
)
from apps.organization.departments.workflows.department_settings_update import (
    DepartmentSettingsUpdateWorkflow,
)
from apps.organization.departments.workflows.department_update import (
    DepartmentUpdateData,
    DepartmentUpdateRequest,
    DepartmentUpdateWorkflow,
)

__all__ = (
    "DepartmentActivationWorkflow",
    "DepartmentCreationData",
    "DepartmentCreationRequest",
    "DepartmentCreationWorkflow",
    "DepartmentDeactivationWorkflow",
    "DepartmentDeletionData",
    "DepartmentDeletionRequest",
    "DepartmentDeletionWorkflow",
    "DepartmentHierarchyManagementWorkflow",
    "DepartmentMemberAssignmentWorkflow",
    "DepartmentRoleManagementWorkflow",
    "DepartmentSettingsUpdateWorkflow",
    "DepartmentUpdateData",
    "DepartmentUpdateRequest",
    "DepartmentUpdateWorkflow",
)

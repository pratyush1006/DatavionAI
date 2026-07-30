"""
Department workflow registration.

Registers department workflows into the DatavionOS
core workflow registry.
"""

from __future__ import annotations

from apps.core.workflows import (
    workflow_registry,
)
from apps.organization.departments.workflows import (
    DepartmentActivationWorkflow,
    DepartmentCreationWorkflow,
    DepartmentDeactivationWorkflow,
    DepartmentDeletionWorkflow,
    DepartmentHierarchyManagementWorkflow,
    DepartmentMemberAssignmentWorkflow,
    DepartmentRoleManagementWorkflow,
    DepartmentSettingsUpdateWorkflow,
    DepartmentUpdateWorkflow,
)


def register_department_workflows() -> None:
    """
    Register department workflows.
    """

    workflows = {
        "department.create": (DepartmentCreationWorkflow),
        "department.update": (DepartmentUpdateWorkflow),
        "department.activate": (DepartmentActivationWorkflow),
        "department.deactivate": (DepartmentDeactivationWorkflow),
        "department.member.assign": (DepartmentMemberAssignmentWorkflow),
        "department.role.manage": (DepartmentRoleManagementWorkflow),
        "department.settings.update": (DepartmentSettingsUpdateWorkflow),
        "department.hierarchy.manage": (DepartmentHierarchyManagementWorkflow),
        "department.delete": (DepartmentDeletionWorkflow),
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(
            name,
        ):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__: tuple[str, ...] = ("register_department_workflows",)

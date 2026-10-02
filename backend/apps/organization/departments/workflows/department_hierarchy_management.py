"""
Department hierarchy management workflow.

Coordinates department tree operations.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.organization.departments.models import (
    Department,
    DepartmentHierarchy,
)
from apps.organization.departments.services import (
    DepartmentHierarchyService,
)
from apps.organization.departments.tasks import (
    index_department,
    synchronize_department,
)

logger = logging.getLogger(__name__)


# ============================================================
# Request
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DepartmentHierarchyManagementRequest:
    """
    Department hierarchy request.
    """

    action: str

    department_id: UUID

    related_department_id: UUID | None = None


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DepartmentHierarchyManagementData:
    """
    Hierarchy workflow result.
    """

    department_id: UUID

    managed: bool

    relation_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class DepartmentHierarchyManagementWorkflow(
    BaseWorkflow[DepartmentHierarchyManagementData],
):
    """
    Manages department hierarchy.
    """

    def __init__(
        self,
        *,
        request: DepartmentHierarchyManagementRequest,
        logger_: logging.Logger | None = None,
    ) -> None:

        super().__init__(
            logger_=logger_,
        )

        self._request = request

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[DepartmentHierarchyManagementData]:
        """
        Execute hierarchy workflow.
        """

        department = Department.objects.get(
            organization_id=context.tenant_id,
            id=self._request.department_id,
        )

        relation = None

        if self._request.action == "add_child":
            child = Department.objects.get(
                organization_id=context.tenant_id,
                id=self._request.related_department_id,
            )

            relation = DepartmentHierarchyService.add_child(
                parent=department,
                child=child,
            )

        elif self._request.action == "move":
            parent = None

            if self._request.related_department_id:
                parent = Department.objects.get(
                    organization_id=context.tenant_id,
                    id=self._request.related_department_id,
                )

            DepartmentHierarchyService.move_department(
                department=department,
                new_parent=parent,
            )

        elif self._request.action == "remove":
            relation = DepartmentHierarchy.objects.get(
                parent=department,
                child_id=self._request.related_department_id,
            )

            DepartmentHierarchyService.remove_relation(
                hierarchy=relation,
            )

        else:
            raise ValueError("Unsupported hierarchy action.")

        self.dispatch_after_commit(
            index_department,
            department_id=department.id,
        )

        self.dispatch_after_commit(
            synchronize_department,
            department_id=department.id,
        )

        logger.info(
            "Department hierarchy managed.",
            extra={
                "department_id": str(
                    department.id,
                ),
                "tenant_id": str(
                    context.tenant_id,
                ),
                "actor_id": str(
                    context.actor_id,
                ),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=DepartmentHierarchyManagementData(
                department_id=department.id,
                managed=True,
                relation_id=(relation.id if relation else None),
            ),
            message=("Department hierarchy updated successfully."),
            code=("department_hierarchy_managed"),
        )


__all__ = (
    "DepartmentHierarchyManagementRequest",
    "DepartmentHierarchyManagementData",
    "DepartmentHierarchyManagementWorkflow",
)

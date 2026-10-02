"""
Department role management workflow.

Coordinates department role operations.
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
from apps.organization.departments.events import (
    DepartmentRoleChangedEvent,
)
from apps.organization.departments.models import (
    Department,
    DepartmentRole,
)
from apps.organization.departments.services import (
    DepartmentRoleService,
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
class DepartmentRoleManagementRequest:
    """
    Department role management request.
    """

    department_id: UUID

    action: str

    role_id: UUID | None = None

    data: dict | None = None


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DepartmentRoleManagementData:
    """
    Role workflow result.
    """

    department_id: UUID

    role_id: UUID

    managed: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class DepartmentRoleManagementWorkflow(
    BaseWorkflow[DepartmentRoleManagementData],
):
    """
    Manages department roles.
    """

    def __init__(
        self,
        *,
        request: DepartmentRoleManagementRequest,
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
    ) -> WorkflowResult[DepartmentRoleManagementData]:
        """
        Execute role management workflow.
        """

        department = Department.objects.get(
            organization_id=context.tenant_id,
            id=self._request.department_id,
        )

        role = None

        if self._request.action == "create":
            role = DepartmentRoleService.create(
                department=department,
                validated_data=(self._request.data or {}),
            )

        elif self._request.action == "update":
            role = DepartmentRole.objects.get(
                id=self._request.role_id,
                department=department,
            )

            role = DepartmentRoleService.update(
                instance=role,
                validated_data=(self._request.data or {}),
            )

        elif self._request.action == "activate":
            role = DepartmentRole.objects.get(
                id=self._request.role_id,
                department=department,
            )

            role = DepartmentRoleService.activate(
                instance=role,
            )

        elif self._request.action == "deactivate":
            role = DepartmentRole.objects.get(
                id=self._request.role_id,
                department=department,
            )

            role = DepartmentRoleService.deactivate(
                instance=role,
            )

        elif self._request.action == "permissions":
            role = DepartmentRole.objects.get(
                id=self._request.role_id,
                department=department,
            )

            role = DepartmentRoleService.update_permissions(
                instance=role,
                permissions=(
                    self._request.data.get(
                        "permissions",
                        [],
                    )
                    if self._request.data
                    else []
                ),
            )

        else:
            raise ValueError("Unsupported department role action.")

        event = DepartmentRoleChangedEvent(
            department_id=department.id,
            role_id=role.id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            index_department,
            department_id=department.id,
        )

        self.dispatch_after_commit(
            synchronize_department,
            department_id=department.id,
        )

        logger.info(
            "Department role managed.",
            extra={
                "department_id": str(
                    department.id,
                ),
                "role_id": str(
                    role.id,
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
            data=DepartmentRoleManagementData(
                department_id=department.id,
                role_id=role.id,
                managed=True,
                event_id=event.event_id,
            ),
            message=("Department role managed successfully."),
            code=("department_role_managed"),
        )


__all__ = (
    "DepartmentRoleManagementRequest",
    "DepartmentRoleManagementData",
    "DepartmentRoleManagementWorkflow",
)

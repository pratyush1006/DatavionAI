"""
Department creation workflow.

Coordinates department creation process.

Responsibilities:

- Resolve actor
- Resolve organization
- Validate RBAC policy
- Execute department service
- Publish domain event
- Dispatch post commit tasks
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.organization.departments.events import (
    DepartmentCreatedEvent,
)
from apps.organization.departments.policies import (
    DepartmentPolicy,
)
from apps.organization.departments.services import (
    create_department,
)
from apps.organization.departments.tasks import (
    index_department,
    send_department_created_notification,
    synchronize_department,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DepartmentCreationRequest:
    """
    Department creation request.
    """

    organization_id: UUID

    name: str

    code: str

    description: str | None = None

    department_type: str | None = None

    phone: str | None = None

    email: str | None = None

    location: str | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DepartmentCreationData:
    """
    Department creation result.
    """

    department_id: UUID

    created: bool

    event_id: UUID | None = None


class DepartmentCreationWorkflow(
    BaseWorkflow[DepartmentCreationData],
):
    """
    Creates department.

    Flow:

        Actor
          |
          v
        RBAC Policy
          |
          v
        Domain Service
          |
          v
        Domain Event
          |
          v
        Async Tasks
    """

    def __init__(
        self,
        *,
        request: DepartmentCreationRequest,
        policy: DepartmentPolicy | None = None,
    ) -> None:

        super().__init__()

        self._request = request

        self._policy = policy or DepartmentPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[DepartmentCreationData]:
        """
        Execute department creation.
        """

        from apps.platform.accounts.models import User
        from apps.platform.organizations.models import Organization

        actor = User.objects.get(
            id=context.actor_id,
        )

        organization = Organization.objects.get(
            id=self._request.organization_id,
        )

        #
        # RBAC authorization
        #
        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to create department.",
            )

        #
        # Domain service
        #
        department = create_department(
            validated_data={
                "organization": organization,
                "name": self._request.name,
                "code": self._request.code,
                "description": self._request.description,
                "department_type": self._request.department_type,
                "phone": self._request.phone,
                "email": self._request.email,
                "location": self._request.location,
            },
        )

        #
        # Domain event
        #
        event = DepartmentCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            department_id=department.id,
            organization_id=organization.id,
        )

        self.publish_after_commit(
            event,
        )

        #
        # Background processing
        #
        self.dispatch_after_commit(
            index_department,
            department_id=department.id,
        )

        self.dispatch_after_commit(
            synchronize_department,
            department_id=department.id,
        )

        self.dispatch_after_commit(
            send_department_created_notification,
            department_id=department.id,
        )

        return WorkflowResult.ok(
            context=context,
            data=DepartmentCreationData(
                department_id=department.id,
                created=True,
                event_id=event.event_id,
            ),
            message=("Department created successfully."),
            code=("department_created"),
        )


__all__ = (
    "DepartmentCreationRequest",
    "DepartmentCreationData",
    "DepartmentCreationWorkflow",
)

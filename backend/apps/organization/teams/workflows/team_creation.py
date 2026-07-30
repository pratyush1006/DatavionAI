"""
Team creation workflow.

Coordinates team creation process.

Responsibilities:

- Resolve organization
- Validate domain rules
- Execute team service
- Publish domain event
- Dispatch post commit tasks

Authorization is handled by RBAC permission classes.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.organization.teams.events import (
    TeamCreatedEvent,
)
from apps.organization.teams.policies import (
    TeamPolicy,
)
from apps.organization.teams.services import (
    create_team,
)
from apps.organization.teams.tasks import (
    index_team,
    send_team_created_notification,
    synchronize_team,
)
from apps.platform.organizations.models import (
    Organization,
)

# ============================================================
# Request
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TeamCreationRequest:
    """
    Team creation request.
    """

    organization_id: UUID

    name: str

    code: str

    description: str | None = None

    team_type: str | None = None


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TeamCreationData:
    """
    Team creation result.
    """

    team_id: UUID

    created: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class TeamCreationWorkflow(
    BaseWorkflow[TeamCreationData],
):
    """
    Creates team.

    Flow:

        RBAC Permission
              |
              v
        Workflow
              |
              v
        Domain Policy
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
        request: TeamCreationRequest,
        policy: TeamPolicy | None = None,
    ) -> None:

        super().__init__()

        self._request = request

        self._policy = policy or TeamPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[TeamCreationData]:
        """
        Execute team creation workflow.
        """

        organization = Organization.objects.get(
            id=self._request.organization_id,
        )

        #
        # Domain validation
        #

        if not self._policy.validate_organization(
            organization=organization,
        ):
            raise ValueError(
                "Invalid organization for team creation.",
            )

        #
        # Domain service
        #

        team = create_team(
            validated_data={
                "organization": organization,
                "name": self._request.name,
                "code": self._request.code,
                "description": self._request.description,
                "team_type": self._request.team_type,
            },
        )

        #
        # Domain event
        #

        event = TeamCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            team_id=team.id,
            organization_id=organization.id,
        )

        self.publish_after_commit(
            event,
        )

        #
        # Background processing
        #

        self.dispatch_after_commit(
            index_team,
            team_id=team.id,
        )

        self.dispatch_after_commit(
            synchronize_team,
            team_id=team.id,
        )

        self.dispatch_after_commit(
            send_team_created_notification,
            team_id=team.id,
        )

        return WorkflowResult.ok(
            context=context,
            data=TeamCreationData(
                team_id=team.id,
                created=True,
                event_id=event.event_id,
            ),
            message=("Team created successfully."),
            code=("team_created"),
        )


__all__ = (
    "TeamCreationRequest",
    "TeamCreationData",
    "TeamCreationWorkflow",
)

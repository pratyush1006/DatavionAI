"""
Team deletion workflow.

Handles team deletion lifecycle.

Responsibilities:

- Tenant scoped team lookup
- Domain policy validation
- Execute delete service
- Publish team deleted event
- Schedule cleanup tasks
- Return workflow result
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
from apps.organization.teams.events import (
    TeamDeletedEvent,
)
from apps.organization.teams.models import (
    Team,
)
from apps.organization.teams.policies import (
    TeamPolicy,
)
from apps.organization.teams.services import (
    delete_team,
)
from apps.organization.teams.tasks import (
    remove_team_index,
    send_team_deleted_notification,
    synchronize_team,
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
class TeamDeletionRequest:
    """
    Team deletion request.
    """

    team_id: UUID


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TeamDeletionData:
    """
    Team deletion result.
    """

    team_id: UUID

    deleted: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class TeamDeletionWorkflow(
    BaseWorkflow[TeamDeletionData],
):
    """
    Deletes team.

    Workflow:

        Tenant Context
              |
              v
        Team Lookup
              |
              v
        Domain Policy
              |
              v
        Delete Service
              |
              v
        Domain Event
              |
              v
        Background Tasks
    """

    def __init__(
        self,
        *,
        request: TeamDeletionRequest,
        policy: TeamPolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:

        super().__init__(
            logger_=logger_,
        )

        self._request = request

        self._policy = policy or TeamPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[TeamDeletionData]:
        """
        Execute team deletion workflow.
        """

        team = Team.objects.get(
            id=self._request.team_id,
            organization__tenant_id=context.tenant_id,
        )

        team_id = team.id

        organization_id = team.organization_id

        #
        # Domain validation
        #

        if not self._policy.can_delete(
            team=team,
        ):
            raise ValueError(
                "Team cannot be deleted.",
            )

        #
        # Domain service
        #

        delete_team(
            instance=team,
        )

        #
        # Domain event
        #

        event = TeamDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            team_id=team_id,
            organization_id=organization_id,
        )

        self.publish_after_commit(
            event,
        )

        #
        # Background processing
        #

        self.dispatch_after_commit(
            send_team_deleted_notification,
            team_id=team_id,
        )

        self.dispatch_after_commit(
            remove_team_index,
            team_id=team_id,
        )

        self.dispatch_after_commit(
            synchronize_team,
            team_id=team_id,
        )

        logger.info(
            "Team deleted.",
            extra={
                "team_id": str(
                    team_id,
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
            data=TeamDeletionData(
                team_id=team_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message=("Team deleted successfully."),
            code=("team_deleted"),
        )


__all__ = (
    "TeamDeletionRequest",
    "TeamDeletionData",
    "TeamDeletionWorkflow",
)

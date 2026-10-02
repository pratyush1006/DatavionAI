"""
Team update workflow.

Coordinates team updates using:

- Tenant scoped lookup
- Domain policy validation
- Domain service
- Domain event
- Post commit tasks
- Workflow result
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
    TeamUpdatedEvent,
)
from apps.organization.teams.models import (
    Team,
)
from apps.organization.teams.policies import (
    TeamPolicy,
)
from apps.organization.teams.services import (
    update_team,
)
from apps.organization.teams.tasks import (
    index_team,
    send_team_updated_notification,
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
class TeamUpdateRequest:
    """
    Team update request.
    """

    team_id: UUID

    data: dict


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TeamUpdateData:
    """
    Team update result.
    """

    team_id: UUID

    updated: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class TeamUpdateWorkflow(
    BaseWorkflow[TeamUpdateData],
):
    """
    Updates team.

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
        Domain Service
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
        request: TeamUpdateRequest,
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
    ) -> WorkflowResult[TeamUpdateData]:
        """
        Execute team update.
        """

        team = Team.objects.get(
            id=self._request.team_id,
            organization__tenant_id=context.tenant_id,
        )

        #
        # Domain validation
        #

        if not self._policy.validate_organization_boundary(
            team=team,
            organization=team.organization,
        ):
            raise ValueError(
                "Team organization boundary violation.",
            )

        #
        # Domain service
        #

        team = update_team(
            instance=team,
            validated_data=self._request.data,
        )

        #
        # Domain event
        #

        event = TeamUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            team_id=team.id,
            organization_id=team.organization_id,
        )

        self.publish_after_commit(
            event,
        )

        #
        # Background processing
        #

        self.dispatch_after_commit(
            send_team_updated_notification,
            team_id=team.id,
        )

        self.dispatch_after_commit(
            index_team,
            team_id=team.id,
        )

        self.dispatch_after_commit(
            synchronize_team,
            team_id=team.id,
        )

        logger.info(
            "Team updated.",
            extra={
                "team_id": str(
                    team.id,
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
            data=TeamUpdateData(
                team_id=team.id,
                updated=True,
                event_id=event.event_id,
            ),
            message=("Team updated successfully."),
            code=("team_updated"),
        )


__all__ = (
    "TeamUpdateRequest",
    "TeamUpdateData",
    "TeamUpdateWorkflow",
)

"""
DatavionOS SaaS Billing Plan event handlers.

Handles:

- Plan created
- Plan updated
- Plan activated
- Plan deactivated
- Plan archived

Architecture:

Domain Event
      |
Plan Handler
      |
Audit
Analytics
Automation
"""

from __future__ import annotations

import logging

from apps.platform.saas_billing.events.plan_events import (
    PlanActivated,
    PlanArchived,
    PlanCreated,
    PlanDeactivated,
    PlanUpdated,
)

logger = logging.getLogger(__name__)


def handle_plan_created(
    event: PlanCreated,
) -> None:
    """
    Handle plan creation event.
    """

    logger.info(
        "Plan created: %s",
        event.aggregate_id,
    )


def handle_plan_updated(
    event: PlanUpdated,
) -> None:
    """
    Handle plan update event.
    """

    logger.info(
        "Plan updated: %s",
        event.aggregate_id,
    )


def handle_plan_activated(
    event: PlanActivated,
) -> None:
    """
    Handle plan activation event.
    """

    logger.info(
        "Plan activated: %s",
        event.aggregate_id,
    )


def handle_plan_deactivated(
    event: PlanDeactivated,
) -> None:
    """
    Handle plan deactivation event.
    """

    logger.info(
        "Plan deactivated: %s",
        event.aggregate_id,
    )


def handle_plan_archived(
    event: PlanArchived,
) -> None:
    """
    Handle plan archive event.
    """

    logger.info(
        "Plan archived: %s",
        event.aggregate_id,
    )


__all__ = [
    "handle_plan_created",
    "handle_plan_updated",
    "handle_plan_activated",
    "handle_plan_deactivated",
    "handle_plan_archived",
]

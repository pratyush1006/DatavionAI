"""
SaaS Billing Plan domain events.

Events:

- Plan Created
- Plan Updated
- Plan Activated
- Plan Deactivated
- Plan Archived
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.platform.saas_billing.events.base import (
    DomainEvent,
)


@dataclass(
    frozen=True,
)
class PlanCreated(
    DomainEvent,
):
    """
    Published when a SaaS plan is created.
    """

    event_type: str = "plan.created"


@dataclass(
    frozen=True,
)
class PlanUpdated(
    DomainEvent,
):
    """
    Published when a SaaS plan is updated.
    """

    event_type: str = "plan.updated"


@dataclass(
    frozen=True,
)
class PlanActivated(
    DomainEvent,
):
    """
    Published when a SaaS plan is activated.
    """

    event_type: str = "plan.activated"


@dataclass(
    frozen=True,
)
class PlanDeactivated(
    DomainEvent,
):
    """
    Published when a SaaS plan is deactivated.
    """

    event_type: str = "plan.deactivated"


@dataclass(
    frozen=True,
)
class PlanArchived(
    DomainEvent,
):
    """
    Published when a SaaS plan is archived.
    """

    event_type: str = "plan.archived"


__all__ = [
    "PlanCreated",
    "PlanUpdated",
    "PlanActivated",
    "PlanDeactivated",
    "PlanArchived",
]

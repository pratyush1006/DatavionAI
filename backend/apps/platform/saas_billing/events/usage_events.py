"""
Usage domain events.

Events emitted from DatavionOS
usage metering lifecycle.

Events:

- UsageRecorded
- UsageEvaluated
- UsageLimitExceeded
- UsageCharged
"""

from __future__ import annotations

from .base import DomainEvent


class UsageRecorded(
    DomainEvent,
):
    """
    Fired when resource usage is captured.

    Consumers:

    - Usage Evaluation
    - Analytics
    - Billing Engine
    """

    event_name = "usage.recorded"


class UsageEvaluated(
    DomainEvent,
):
    """
    Fired after usage is evaluated
    against subscription limits.

    Consumers:

    - Billing Engine
    - Notification Service
    - Analytics
    """

    event_name = "usage.evaluated"


class UsageLimitExceeded(
    DomainEvent,
):
    """
    Fired when organization exceeds
    subscription quota.

    Consumers:

    - Notification Service
    - Upgrade Workflow
    - Billing Engine
    """

    event_name = "usage.limit_exceeded"


class UsageCharged(
    DomainEvent,
):
    """
    Fired when billable usage charge
    is calculated.

    Consumers:

    - Invoice Generation
    - Accounting Service
    - Revenue Analytics
    """

    event_name = "usage.charged"


__all__ = [
    "UsageRecorded",
    "UsageEvaluated",
    "UsageLimitExceeded",
    "UsageCharged",
]

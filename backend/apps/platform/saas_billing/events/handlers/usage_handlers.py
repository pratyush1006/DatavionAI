"""
Usage event handlers.

Consumes usage lifecycle events.

Events:

- UsageRecorded
- UsageLimitExceeded
- UsageCharged
"""

from __future__ import annotations

import logging

from ..usage_events import (
    UsageCharged,
    UsageLimitExceeded,
    UsageRecorded,
)

logger = logging.getLogger(
    __name__,
)


def handle_usage_recorded(
    event: UsageRecorded,
) -> None:
    """
    Handle usage recording.

    Future actions:

    - Update usage analytics
    - Refresh dashboard metrics
    - Validate quotas
    - Trigger automation
    """

    logger.info(
        "Usage recorded: %s",
        event.aggregate_id,
    )


def handle_usage_limit_exceeded(
    event: UsageLimitExceeded,
) -> None:
    """
    Handle exceeded subscription limit.

    Future actions:

    - Send notification
    - Trigger upgrade workflow
    - Create billing alert
    """

    logger.info(
        "Usage limit exceeded: %s",
        event.aggregate_id,
    )


def handle_usage_charged(
    event: UsageCharged,
) -> None:
    """
    Handle billable usage charge.

    Future actions:

    - Generate invoice line item
    - Update revenue analytics
    - Create accounting record
    """

    logger.info(
        "Usage charged: %s",
        event.aggregate_id,
    )


__all__ = [
    "handle_usage_recorded",
    "handle_usage_limit_exceeded",
    "handle_usage_charged",
]

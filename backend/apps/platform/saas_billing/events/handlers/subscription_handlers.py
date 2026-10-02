"""
Subscription event handlers.

Consumes:

- SubscriptionCreated
- SubscriptionActivated
- SubscriptionRenewed
- SubscriptionCancelled
"""

from __future__ import annotations

import logging

from ..subscription_events import (
    SubscriptionActivated,
    SubscriptionCancelled,
    SubscriptionCreated,
    SubscriptionRenewed,
)

logger = logging.getLogger(
    __name__,
)


def handle_subscription_created(
    event: SubscriptionCreated,
) -> None:
    """
    Handle subscription creation.

    Future actions:

    - Create entitlements
    - Update bootstrap cache
    - Send welcome notification
    """

    logger.info(
        "Subscription created: %s",
        event.aggregate_id,
    )


def handle_subscription_activated(
    event: SubscriptionActivated,
) -> None:
    """
    Handle activation event.

    Future actions:

    - Enable modules
    - Activate organization access
    """

    logger.info(
        "Subscription activated: %s",
        event.aggregate_id,
    )


def handle_subscription_renewed(
    event: SubscriptionRenewed,
) -> None:
    """
    Handle renewal event.
    """

    logger.info(
        "Subscription renewed: %s",
        event.aggregate_id,
    )


def handle_subscription_cancelled(
    event: SubscriptionCancelled,
) -> None:
    """
    Handle cancellation event.

    Future actions:

    - Disable auto renewal
    - Notify organization
    """

    logger.info(
        "Subscription cancelled: %s",
        event.aggregate_id,
    )


__all__ = [
    "handle_subscription_created",
    "handle_subscription_activated",
    "handle_subscription_renewed",
    "handle_subscription_cancelled",
]

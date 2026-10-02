"""
Subscription domain events.

Events emitted from DatavionOS
subscription lifecycle.

Events:

- SubscriptionCreated
- SubscriptionActivated
- SubscriptionRenewed
- SubscriptionUpgraded
- SubscriptionDowngraded
- SubscriptionCancelled
- SubscriptionExpired
"""

from __future__ import annotations

from .base import DomainEvent


class SubscriptionCreated(
    DomainEvent,
):
    """
    Fired when subscription is created.

    Consumers:

    - Entitlement Service
    - Platform Bootstrap
    - Notification Service
    - Audit Service
    """

    event_name = "subscription.created"


class SubscriptionActivated(
    DomainEvent,
):
    """
    Fired when subscription becomes active.
    """

    event_name = "subscription.activated"


class SubscriptionRenewed(
    DomainEvent,
):
    """
    Fired after successful renewal.
    """

    event_name = "subscription.renewed"


class SubscriptionUpgraded(
    DomainEvent,
):
    """
    Fired when organization upgrades plan.
    """

    event_name = "subscription.upgraded"


class SubscriptionDowngraded(
    DomainEvent,
):
    """
    Fired when organization downgrades plan.
    """

    event_name = "subscription.downgraded"


class SubscriptionCancelled(
    DomainEvent,
):
    """
    Fired when subscription is cancelled.
    """

    event_name = "subscription.cancelled"


class SubscriptionExpired(
    DomainEvent,
):
    """
    Fired when subscription expires.
    """

    event_name = "subscription.expired"


__all__ = [
    "SubscriptionCreated",
    "SubscriptionActivated",
    "SubscriptionRenewed",
    "SubscriptionUpgraded",
    "SubscriptionDowngraded",
    "SubscriptionCancelled",
    "SubscriptionExpired",
]

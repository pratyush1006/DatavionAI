"""
Billing account domain events.

Events emitted from DatavionOS
SaaS billing account lifecycle.

Events:

- BillingAccountCreated
- BillingAccountUpdated
- BillingAccountSuspended
- BillingAccountClosed
"""

from __future__ import annotations

from .base import DomainEvent


class BillingAccountCreated(
    DomainEvent,
):
    """
    Fired when billing account is created.

    Consumers:

    - Audit Service
    - Notification Service
    - Analytics Service
    - Subscription Provisioning
    """

    event_name = "billing_account.created"


class BillingAccountUpdated(
    DomainEvent,
):
    """
    Fired when billing profile changes.
    """

    event_name = "billing_account.updated"


class BillingAccountSuspended(
    DomainEvent,
):
    """
    Fired when billing account is suspended.
    """

    event_name = "billing_account.suspended"


class BillingAccountClosed(
    DomainEvent,
):
    """
    Fired when billing account is closed.
    """

    event_name = "billing_account.closed"


__all__ = [
    "BillingAccountCreated",
    "BillingAccountUpdated",
    "BillingAccountSuspended",
    "BillingAccountClosed",
]

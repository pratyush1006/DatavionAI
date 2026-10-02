"""
Payment domain events.

Events emitted from DatavionOS
payment lifecycle.

Events:

- PaymentCreated
- PaymentProcessingStarted
- PaymentSucceeded
- PaymentFailed
- PaymentRefunded
- PaymentReconciled
"""

from __future__ import annotations

from .base import DomainEvent


class PaymentCreated(
    DomainEvent,
):
    """
    Fired when payment transaction
    is created.

    Consumers:

    - Payment Gateway
    - Audit Service
    - Analytics Service
    """

    event_name = "payment.created"


class PaymentProcessingStarted(
    DomainEvent,
):
    """
    Fired when payment processing
    starts.
    """

    event_name = "payment.processing_started"


class PaymentSucceeded(
    DomainEvent,
):
    """
    Fired when payment succeeds.

    Consumers:

    - Invoice Service
    - Subscription Service
    - Receipt Service
    - Notification Service
    """

    event_name = "payment.succeeded"


class PaymentFailed(
    DomainEvent,
):
    """
    Fired when payment fails.
    """

    event_name = "payment.failed"


class PaymentRefunded(
    DomainEvent,
):
    """
    Fired when payment refund
    completes.
    """

    event_name = "payment.refunded"


class PaymentReconciled(
    DomainEvent,
):
    """
    Fired after gateway reconciliation.
    """

    event_name = "payment.reconciled"


__all__ = [
    "PaymentCreated",
    "PaymentProcessingStarted",
    "PaymentSucceeded",
    "PaymentFailed",
    "PaymentRefunded",
    "PaymentReconciled",
]

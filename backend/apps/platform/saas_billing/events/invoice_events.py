"""
Invoice domain events.

Events emitted from DatavionOS
invoice lifecycle.

Events:

- InvoiceGenerated
- InvoiceIssued
- InvoiceSent
- InvoiceFinalized
- InvoicePaid
- InvoiceCancelled
- InvoiceRefunded
"""

from __future__ import annotations

from .base import DomainEvent


class InvoiceGenerated(
    DomainEvent,
):
    """
    Fired when invoice is generated.

    Consumers:

    - Payment Workflow
    - Notification Service
    - Accounting Service
    - Audit Service
    """

    event_name = "invoice.generated"


class InvoiceIssued(
    DomainEvent,
):
    """
    Fired when invoice is officially issued.
    """

    event_name = "invoice.issued"


class InvoiceSent(
    DomainEvent,
):
    """
    Fired when invoice is delivered
    to customer organization.
    """

    event_name = "invoice.sent"


class InvoiceFinalized(
    DomainEvent,
):
    """
    Fired when invoice is finalized
    and ready for payment collection.

    Consumers:

    - Payment Workflow
    - Accounting Service
    - Notification Service
    - Audit Service
    """

    event_name = "invoice.finalized"


class InvoicePaid(
    DomainEvent,
):
    """
    Fired when invoice payment is completed.

    Consumers:

    - Subscription Activation
    - Receipt Generation
    - Accounting
    - Notifications
    """

    event_name = "invoice.paid"


class InvoiceCancelled(
    DomainEvent,
):
    """
    Fired when invoice is cancelled.
    """

    event_name = "invoice.cancelled"


class InvoiceRefunded(
    DomainEvent,
):
    """
    Fired when invoice is refunded.
    """

    event_name = "invoice.refunded"


__all__ = [
    "InvoiceGenerated",
    "InvoiceIssued",
    "InvoiceSent",
    "InvoiceFinalized",
    "InvoicePaid",
    "InvoiceCancelled",
    "InvoiceRefunded",
]

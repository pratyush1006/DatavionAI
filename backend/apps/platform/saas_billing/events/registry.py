"""
SaaS Billing event registry.

Registers domain events with their handlers.

Architecture:

Domain Event
      |
Event Registry
      |
Event Dispatcher
      |
Handler
      |
Audit / Notification / Analytics / Automation
"""

from __future__ import annotations

from .dispatcher import (
    EventDispatcher,
)
from .handlers import (
    handle_invoice_cancelled,
    handle_invoice_generated,
    handle_invoice_issued,
    handle_invoice_paid,
    handle_invoice_refunded,
    handle_invoice_sent,
    handle_payment_created,
    handle_payment_failed,
    handle_payment_processing_started,
    handle_payment_reconciled,
    handle_payment_refunded,
    handle_payment_succeeded,
    handle_plan_activated,
    handle_plan_archived,
    handle_plan_created,
    handle_plan_deactivated,
    handle_plan_updated,
    handle_subscription_activated,
    handle_subscription_cancelled,
    handle_subscription_created,
    handle_subscription_renewed,
    handle_usage_charged,
    handle_usage_limit_exceeded,
    handle_usage_recorded,
)
from .invoice_events import (
    InvoiceCancelled,
    InvoiceGenerated,
    InvoiceIssued,
    InvoicePaid,
    InvoiceRefunded,
    InvoiceSent,
)
from .payment_events import (
    PaymentCreated,
    PaymentFailed,
    PaymentProcessingStarted,
    PaymentReconciled,
    PaymentRefunded,
    PaymentSucceeded,
)
from .plan_events import (
    PlanActivated,
    PlanArchived,
    PlanCreated,
    PlanDeactivated,
    PlanUpdated,
)
from .subscription_events import (
    SubscriptionActivated,
    SubscriptionCancelled,
    SubscriptionCreated,
    SubscriptionRenewed,
)
from .usage_events import (
    UsageCharged,
    UsageLimitExceeded,
    UsageRecorded,
)


def register_billing_events() -> None:
    """
    Register all SaaS Billing event handlers.

    Called during application startup.
    """

    # ------------------------------------------------------------------
    # Plan
    # ------------------------------------------------------------------

    EventDispatcher.register(
        PlanCreated,
        handle_plan_created,
    )

    EventDispatcher.register(
        PlanUpdated,
        handle_plan_updated,
    )

    EventDispatcher.register(
        PlanActivated,
        handle_plan_activated,
    )

    EventDispatcher.register(
        PlanDeactivated,
        handle_plan_deactivated,
    )

    EventDispatcher.register(
        PlanArchived,
        handle_plan_archived,
    )

    # ------------------------------------------------------------------
    # Subscription
    # ------------------------------------------------------------------

    EventDispatcher.register(
        SubscriptionCreated,
        handle_subscription_created,
    )

    EventDispatcher.register(
        SubscriptionActivated,
        handle_subscription_activated,
    )

    EventDispatcher.register(
        SubscriptionRenewed,
        handle_subscription_renewed,
    )

    EventDispatcher.register(
        SubscriptionCancelled,
        handle_subscription_cancelled,
    )

    # ------------------------------------------------------------------
    # Invoice
    # ------------------------------------------------------------------

    EventDispatcher.register(
        InvoiceGenerated,
        handle_invoice_generated,
    )

    EventDispatcher.register(
        InvoiceIssued,
        handle_invoice_issued,
    )

    EventDispatcher.register(
        InvoiceSent,
        handle_invoice_sent,
    )

    EventDispatcher.register(
        InvoicePaid,
        handle_invoice_paid,
    )

    EventDispatcher.register(
        InvoiceCancelled,
        handle_invoice_cancelled,
    )

    EventDispatcher.register(
        InvoiceRefunded,
        handle_invoice_refunded,
    )

    # ------------------------------------------------------------------
    # Payment
    # ------------------------------------------------------------------

    EventDispatcher.register(
        PaymentCreated,
        handle_payment_created,
    )

    EventDispatcher.register(
        PaymentProcessingStarted,
        handle_payment_processing_started,
    )

    EventDispatcher.register(
        PaymentSucceeded,
        handle_payment_succeeded,
    )

    EventDispatcher.register(
        PaymentFailed,
        handle_payment_failed,
    )

    EventDispatcher.register(
        PaymentRefunded,
        handle_payment_refunded,
    )

    EventDispatcher.register(
        PaymentReconciled,
        handle_payment_reconciled,
    )

    # ------------------------------------------------------------------
    # Usage
    # ------------------------------------------------------------------

    EventDispatcher.register(
        UsageRecorded,
        handle_usage_recorded,
    )

    EventDispatcher.register(
        UsageLimitExceeded,
        handle_usage_limit_exceeded,
    )

    EventDispatcher.register(
        UsageCharged,
        handle_usage_charged,
    )


__all__ = [
    "register_billing_events",
]

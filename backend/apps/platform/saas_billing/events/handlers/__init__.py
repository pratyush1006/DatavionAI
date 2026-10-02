"""
DatavionOS SaaS Billing event handlers.

Central registry for domain event consumers.

Handlers:

- Subscription handlers
- Invoice handlers
- Payment handlers
- Usage handlers
"""

from .invoice_handlers import (
    handle_invoice_cancelled,
    handle_invoice_generated,
    handle_invoice_issued,
    handle_invoice_paid,
    handle_invoice_refunded,
    handle_invoice_sent,
)
from .payment_handlers import (
    handle_payment_created,
    handle_payment_failed,
    handle_payment_processing_started,
    handle_payment_reconciled,
    handle_payment_refunded,
    handle_payment_succeeded,
)
from .plan_handlers import (
    handle_plan_activated,
    handle_plan_archived,
    handle_plan_created,
    handle_plan_deactivated,
    handle_plan_updated,
)
from .subscription_handlers import (
    handle_subscription_activated,
    handle_subscription_cancelled,
    handle_subscription_created,
    handle_subscription_renewed,
)
from .usage_handlers import (
    handle_usage_charged,
    handle_usage_limit_exceeded,
    handle_usage_recorded,
)

__all__ = [
    "handle_subscription_created",
    "handle_subscription_activated",
    "handle_subscription_renewed",
    "handle_subscription_cancelled",
    "handle_invoice_generated",
    "handle_invoice_issued",
    "handle_invoice_sent",
    "handle_invoice_paid",
    "handle_invoice_cancelled",
    "handle_invoice_refunded",
    "handle_payment_created",
    "handle_payment_processing_started",
    "handle_payment_succeeded",
    "handle_payment_failed",
    "handle_payment_refunded",
    "handle_payment_reconciled",
    "handle_usage_recorded",
    "handle_usage_limit_exceeded",
    "handle_usage_charged",
    "handle_plan_created",
    "handle_plan_updated",
    "handle_plan_activated",
    "handle_plan_deactivated",
    "handle_plan_archived",
]

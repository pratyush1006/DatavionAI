"""
DatavionOS SaaS Billing Domain Events.

Central registry for all billing domain events.

Domains:

- Billing Account Events
- Plan Events
- Subscription Events
- Invoice Events
- Payment Events
- Usage Events

Architecture:

Service
    |
Workflow
    |
Domain Event
    |
Event Dispatcher
    |
Handlers
    |
Audit
Notification
Analytics
Automation
"""

from .base import (
    DomainEvent,
)

# ------------------------------------------------------------------
# Billing Account Events
# ------------------------------------------------------------------
from .billing_events import (
    BillingAccountClosed,
    BillingAccountCreated,
    BillingAccountSuspended,
    BillingAccountUpdated,
)

# ------------------------------------------------------------------
# Event Infrastructure
# ------------------------------------------------------------------
from .dispatcher import (
    EventDispatcher,
)

# ------------------------------------------------------------------
# Invoice Events
# ------------------------------------------------------------------
from .invoice_events import (
    InvoiceCancelled,
    InvoiceFinalized,
    InvoiceGenerated,
    InvoiceIssued,
    InvoicePaid,
    InvoiceRefunded,
    InvoiceSent,
)

# ------------------------------------------------------------------
# Payment Events
# ------------------------------------------------------------------
from .payment_events import (
    PaymentCreated,
    PaymentFailed,
    PaymentProcessingStarted,
    PaymentReconciled,
    PaymentRefunded,
    PaymentSucceeded,
)

# ------------------------------------------------------------------
# Plan Events
# ------------------------------------------------------------------
from .plan_events import (
    PlanActivated,
    PlanArchived,
    PlanCreated,
    PlanDeactivated,
    PlanUpdated,
)
from .registry import (
    register_billing_events,
)

# ------------------------------------------------------------------
# Subscription Events
# ------------------------------------------------------------------
from .subscription_events import (
    SubscriptionActivated,
    SubscriptionCancelled,
    SubscriptionCreated,
    SubscriptionDowngraded,
    SubscriptionExpired,
    SubscriptionRenewed,
    SubscriptionUpgraded,
)

# ------------------------------------------------------------------
# Usage Events
# ------------------------------------------------------------------
from .usage_events import (
    UsageCharged,
    UsageEvaluated,
    UsageLimitExceeded,
    UsageRecorded,
)

__all__ = [
    # Base
    "DomainEvent",
    # Billing Account
    "BillingAccountCreated",
    "BillingAccountUpdated",
    "BillingAccountSuspended",
    "BillingAccountClosed",
    # Plan
    "PlanCreated",
    "PlanUpdated",
    "PlanActivated",
    "PlanDeactivated",
    "PlanArchived",
    # Subscription
    "SubscriptionCreated",
    "SubscriptionActivated",
    "SubscriptionRenewed",
    "SubscriptionUpgraded",
    "SubscriptionDowngraded",
    "SubscriptionCancelled",
    "SubscriptionExpired",
    # Invoice
    "InvoiceGenerated",
    "InvoiceIssued",
    "InvoiceSent",
    "InvoiceFinalized",
    "InvoicePaid",
    "InvoiceCancelled",
    "InvoiceRefunded",
    # Payment
    "PaymentCreated",
    "PaymentProcessingStarted",
    "PaymentSucceeded",
    "PaymentFailed",
    "PaymentRefunded",
    "PaymentReconciled",
    # Usage
    "UsageRecorded",
    "UsageEvaluated",
    "UsageLimitExceeded",
    "UsageCharged",
    # Infrastructure
    "EventDispatcher",
    "register_billing_events",
]

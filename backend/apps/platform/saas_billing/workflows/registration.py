"""
DatavionOS SaaS Billing workflow registration.

Registers all billing lifecycle workflows.

Loaded during Django startup.

Domains:

- Subscription
- Invoice
- Payment
- Usage
"""

from __future__ import annotations

from .invoice import (
    FinalizeInvoiceWorkflow,
    GenerateInvoiceWorkflow,
    IssueInvoiceWorkflow,
)
from .payment import (
    ProcessPaymentWorkflow,
    ReconcilePaymentWorkflow,
    RefundPaymentWorkflow,
)
from .registry import (
    WorkflowRegistry,
)
from .subscription import (
    ActivateSubscriptionWorkflow,
    CancelSubscriptionWorkflow,
    CreateSubscriptionWorkflow,
    RenewSubscriptionWorkflow,
)
from .usage import (
    ChargeUsageWorkflow,
    CollectUsageWorkflow,
    EvaluateUsageWorkflow,
)


def register_billing_workflows() -> None:
    """
    Register DatavionOS SaaS billing workflows.
    """

    # Subscription

    WorkflowRegistry.register(
        "subscription.create",
        CreateSubscriptionWorkflow,
    )

    WorkflowRegistry.register(
        "subscription.activate",
        ActivateSubscriptionWorkflow,
    )

    WorkflowRegistry.register(
        "subscription.renew",
        RenewSubscriptionWorkflow,
    )

    WorkflowRegistry.register(
        "subscription.cancel",
        CancelSubscriptionWorkflow,
    )

    # Invoice

    WorkflowRegistry.register(
        "invoice.generate",
        GenerateInvoiceWorkflow,
    )

    WorkflowRegistry.register(
        "invoice.issue",
        IssueInvoiceWorkflow,
    )

    WorkflowRegistry.register(
        "invoice.finalize",
        FinalizeInvoiceWorkflow,
    )

    # Payment

    WorkflowRegistry.register(
        "payment.process",
        ProcessPaymentWorkflow,
    )

    WorkflowRegistry.register(
        "payment.reconcile",
        ReconcilePaymentWorkflow,
    )

    WorkflowRegistry.register(
        "payment.refund",
        RefundPaymentWorkflow,
    )

    # Usage

    WorkflowRegistry.register(
        "usage.collect",
        CollectUsageWorkflow,
    )

    WorkflowRegistry.register(
        "usage.evaluate",
        EvaluateUsageWorkflow,
    )

    WorkflowRegistry.register(
        "usage.charge",
        ChargeUsageWorkflow,
    )


__all__ = [
    "register_billing_workflows",
]

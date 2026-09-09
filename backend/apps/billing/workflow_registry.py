"""
Billing Core workflow registry integration.
"""

from __future__ import annotations

from apps.billing.workflows import (
    ClaimAppealWorkflow,
    ClaimApprovalWorkflow,
    ClaimCreationWorkflow,
    ClaimRejectWorkflow,
    ClaimSettleWorkflow,
    InvoiceCreationWorkflow,
    InvoiceDeleteWorkflow,
    InvoiceUpdateWorkflow,
    InvoiceVoidWorkflow,
    PaymentCreationWorkflow,
)
from apps.core.workflows import workflow_registry


def register_billing_workflows() -> None:
    """Register all Billing Core mutation workflows idempotently."""
    registrations = (
        ("billing.invoice.create", InvoiceCreationWorkflow),
        ("billing.invoice.update", InvoiceUpdateWorkflow),
        ("billing.invoice.delete", InvoiceDeleteWorkflow),
        ("billing.invoice.void", InvoiceVoidWorkflow),
        ("billing.payment.create", PaymentCreationWorkflow),
        ("billing.claim.create", ClaimCreationWorkflow),
        ("billing.claim.approve", ClaimApprovalWorkflow),
        ("billing.claim.reject", ClaimRejectWorkflow),
        ("billing.claim.appeal", ClaimAppealWorkflow),
        ("billing.claim.settle", ClaimSettleWorkflow),
    )
    for name, workflow in registrations:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


register_billing_workflows()


__all__ = ("register_billing_workflows",)

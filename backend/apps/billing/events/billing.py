"""
Billing Core domain events.
"""

from __future__ import annotations

from apps.core.events import DomainEvent


class BillingInvoiceCreatedEvent(DomainEvent):
    """Represent successful invoice creation."""

    event_type = "billing.invoice.created"

    def __init__(self, *, tenant_id, actor_id, invoice_id, patient_id, organization_id):
        """Initialize the event."""
        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "invoice_id": str(invoice_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
            },
        )


class BillingPaymentCreatedEvent(DomainEvent):
    """Represent successful payment creation."""

    event_type = "billing.payment.created"

    def __init__(
        self,
        *,
        tenant_id,
        actor_id,
        payment_id,
        invoice_id,
        patient_id,
        organization_id,
        amount,
    ):
        """Initialize the event."""
        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "payment_id": str(payment_id),
                "invoice_id": str(invoice_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
                "amount": str(amount),
            },
        )


class BillingClaimStatusChangedEvent(DomainEvent):
    """Represent an insurance claim lifecycle transition."""

    event_type = "billing.claim.status_changed"

    def __init__(
        self,
        *,
        tenant_id,
        actor_id,
        claim_id,
        invoice_id,
        patient_id,
        organization_id,
        previous_status,
        status,
    ):
        """Initialize the event."""
        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "claim_id": str(claim_id),
                "invoice_id": str(invoice_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
                "previous_status": previous_status,
                "status": status,
            },
        )


__all__ = (
    "BillingClaimStatusChangedEvent",
    "BillingInvoiceCreatedEvent",
    "BillingPaymentCreatedEvent",
)

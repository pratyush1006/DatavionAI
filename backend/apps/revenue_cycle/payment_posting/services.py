"""Transactional payment posting services."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from .constants import PaymentPostingStatus
from .exceptions import InvalidPaymentPostingTransition
from .models import PaymentPosting
from .selectors import (
    get_deleted_payment_posting_for_update,
    get_payment_posting_for_update,
)


def _validate_amounts(*, amount: Decimal, adjustment_amount: Decimal) -> None:
    """Validate monetary invariants before persistence."""

    if amount <= Decimal("0.00"):
        raise ValueError("Payment amount must be greater than zero.")
    if adjustment_amount < Decimal("0.00"):
        raise ValueError("Adjustment amount cannot be negative.")


@transaction.atomic
def create_payment_posting(
    *, organization, patient, data: dict, actor
) -> PaymentPosting:
    """Create an idempotent payment posting within organization scope."""

    amount = Decimal(str(data["amount"]))
    adjustment_amount = Decimal(str(data.get("adjustment_amount", "0.00")))
    _validate_amounts(amount=amount, adjustment_amount=adjustment_amount)
    posting = PaymentPosting.objects.create(
        organization=organization,
        patient=patient,
        invoice=data.get("invoice"),
        payer_name=data.get("payer_name", ""),
        payer_claim_reference=data.get("payer_claim_reference", ""),
        source=data.get("source", "manual"),
        amount=amount,
        adjustment_amount=adjustment_amount,
        external_reference=data.get("external_reference", ""),
        idempotency_key=data["idempotency_key"],
        notes=data.get("notes", ""),
        posted_by=actor,
    )
    return posting


@transaction.atomic
def update_payment_posting(
    *,
    organization_id: UUID,
    tenant_id: UUID,
    posting_id: UUID,
    data: dict,
) -> PaymentPosting:
    """Update mutable fields under a row lock."""

    posting = get_payment_posting_for_update(
        organization_id=organization_id,
        tenant_id=tenant_id,
        posting_id=posting_id,
    )
    if posting.status != PaymentPostingStatus.PENDING:
        raise InvalidPaymentPostingTransition("Only pending postings may be edited.")
    for field in (
        "payer_name",
        "payer_claim_reference",
        "source",
        "external_reference",
        "notes",
    ):
        if field in data:
            setattr(posting, field, data[field])
    if "amount" in data:
        posting.amount = Decimal(str(data["amount"]))
    if "adjustment_amount" in data:
        posting.adjustment_amount = Decimal(str(data["adjustment_amount"]))
    _validate_amounts(
        amount=posting.amount,
        adjustment_amount=posting.adjustment_amount,
    )
    posting.save()
    return posting


@transaction.atomic
def post_payment(
    *, organization_id: UUID, tenant_id: UUID, posting_id: UUID, actor
) -> PaymentPosting:
    """Post a pending payment under a database row lock."""

    posting = get_payment_posting_for_update(
        organization_id=organization_id,
        tenant_id=tenant_id,
        posting_id=posting_id,
    )
    if posting.status != PaymentPostingStatus.PENDING:
        raise InvalidPaymentPostingTransition("Only pending postings may be posted.")
    posting.status = PaymentPostingStatus.POSTED
    posting.posted_at = timezone.now()
    posting.posted_by = actor
    posting.save(update_fields=("status", "posted_at", "posted_by", "updated_at"))
    return posting


@transaction.atomic
def reverse_payment(
    *,
    organization_id: UUID,
    tenant_id: UUID,
    posting_id: UUID,
    reason: str,
) -> PaymentPosting:
    """Reverse a posted payment under a database row lock."""

    posting = get_payment_posting_for_update(
        organization_id=organization_id,
        tenant_id=tenant_id,
        posting_id=posting_id,
    )
    if posting.status != PaymentPostingStatus.POSTED:
        raise InvalidPaymentPostingTransition("Only posted payments may be reversed.")
    if not reason.strip():
        raise ValueError("A reversal reason is required.")
    posting.status = PaymentPostingStatus.REVERSED
    posting.reversed_at = timezone.now()
    posting.reversal_reason = reason.strip()
    posting.save(
        update_fields=("status", "reversed_at", "reversal_reason", "updated_at")
    )
    return posting


@transaction.atomic
def delete_payment_posting(
    *, organization_id: UUID, tenant_id: UUID, posting_id: UUID, user_id: UUID
) -> PaymentPosting:
    """Soft-delete a pending payment posting under a row lock."""

    posting = get_payment_posting_for_update(
        organization_id=organization_id,
        tenant_id=tenant_id,
        posting_id=posting_id,
    )
    if posting.status != PaymentPostingStatus.PENDING:
        raise InvalidPaymentPostingTransition("Only pending postings may be deleted.")
    posting.soft_delete(user_id=user_id)
    return posting


@transaction.atomic
def restore_payment_posting(
    *, organization_id: UUID, tenant_id: UUID, posting_id: UUID
) -> PaymentPosting:
    """Restore a deleted payment posting under a row lock."""

    posting = get_deleted_payment_posting_for_update(
        organization_id=organization_id,
        tenant_id=tenant_id,
        posting_id=posting_id,
    )
    posting.restore()
    return posting


__all__ = (
    "create_payment_posting",
    "delete_payment_posting",
    "post_payment",
    "restore_payment_posting",
    "reverse_payment",
    "update_payment_posting",
)

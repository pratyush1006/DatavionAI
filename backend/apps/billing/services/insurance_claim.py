"""
Billing Core Insurance Claim service.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.billing.constants import ClaimStatus
from apps.billing.exceptions import (
    BillingFinancialInvariantError,
    BillingLifecycleError,
)
from apps.billing.models import InsuranceClaim, Invoice


class InsuranceClaimService:
    """Mutate insurance claims and settlement aggregates."""

    @staticmethod
    @transaction.atomic
    def create(
        *,
        organization,
        patient,
        invoice,
        data,
        performed_by,
    ) -> InsuranceClaim:
        """Submit a claim after validating aggregate ownership."""
        if invoice.organization_id != organization.pk:
            raise BillingFinancialInvariantError(
                "Claim and invoice organizations must match.",
            )
        if invoice.patient_id != patient.pk:
            raise BillingFinancialInvariantError(
                "Claim and invoice patients must match.",
            )

        claim = InsuranceClaim(
            organization=organization,
            patient=patient,
            invoice=invoice,
            insurance_provider=data["insurance_provider"],
            policy_number=data["policy_number"],
            claim_number=data["claim_number"],
            claim_amount=data["claim_amount"],
            status=ClaimStatus.SUBMITTED,
        )
        claim.full_clean()
        claim.save()

        return claim

    @staticmethod
    @transaction.atomic
    def approve(
        *,
        claim: InsuranceClaim,
        approved_amount: Decimal,
        performed_by,
    ) -> InsuranceClaim:
        """Approve a submitted or appealed claim."""
        locked = InsuranceClaim.objects.select_for_update().get(pk=claim.pk)

        if locked.status not in (
            ClaimStatus.SUBMITTED,
            ClaimStatus.APPEALED,
        ):
            raise BillingLifecycleError(
                "Only submitted or appealed claims can be approved.",
            )

        amount = Decimal(
            str(approved_amount),
        )
        if amount <= Decimal("0.00") or amount > locked.claim_amount:
            raise BillingFinancialInvariantError(
                "Approved amount must be positive and not exceed claim amount.",
            )

        locked.approved_amount = amount
        locked.status = (
            ClaimStatus.APPROVED
            if amount == locked.claim_amount
            else ClaimStatus.PARTIALLY_APPROVED
        )
        locked.rejection_reason = ""
        locked.full_clean()
        locked.save()

        return locked

    @staticmethod
    @transaction.atomic
    def reject(
        *,
        claim: InsuranceClaim,
        rejection_reason: str,
        performed_by,
    ) -> InsuranceClaim:
        """Reject a submitted or appealed claim."""
        locked = InsuranceClaim.objects.select_for_update().get(pk=claim.pk)

        if locked.status not in (
            ClaimStatus.SUBMITTED,
            ClaimStatus.APPEALED,
        ):
            raise BillingLifecycleError(
                "Only submitted or appealed claims can be rejected.",
            )

        reason = rejection_reason.strip()
        if not reason:
            raise BillingLifecycleError(
                "A rejection reason is required.",
            )

        locked.status = ClaimStatus.REJECTED
        locked.rejection_reason = reason
        locked.full_clean()
        locked.save()

        return locked

    @staticmethod
    @transaction.atomic
    def appeal(
        *,
        claim: InsuranceClaim,
        performed_by,
    ) -> InsuranceClaim:
        """Appeal a rejected claim."""
        locked = InsuranceClaim.objects.select_for_update().get(pk=claim.pk)

        if locked.status != ClaimStatus.REJECTED:
            raise BillingLifecycleError(
                "Only rejected claims can be appealed.",
            )

        locked.status = ClaimStatus.APPEALED
        locked.rejection_reason = ""
        locked.full_clean()
        locked.save()

        return locked

    @staticmethod
    @transaction.atomic
    def settle(
        *,
        claim: InsuranceClaim,
        performed_by,
    ) -> InsuranceClaim:
        """Settle an approved claim and apply its proceeds to the invoice."""
        locked_claim = (
            InsuranceClaim.objects.select_for_update()
            .select_related("invoice")
            .get(pk=claim.pk)
        )

        if locked_claim.status not in (
            ClaimStatus.APPROVED,
            ClaimStatus.PARTIALLY_APPROVED,
        ):
            raise BillingLifecycleError(
                "Only approved claims can be settled.",
            )

        if locked_claim.approved_amount is None:
            raise BillingFinancialInvariantError(
                "Approved claim amount is required for settlement.",
            )

        invoice = Invoice.objects.select_for_update().get(pk=locked_claim.invoice_id)

        applied = min(
            locked_claim.approved_amount,
            invoice.balance_amount,
        )

        invoice.paid_amount += applied
        invoice.balance_amount = invoice.total_amount - invoice.paid_amount
        invoice.recalculate_status()
        invoice.full_clean()
        invoice.save(
            update_fields=(
                "paid_amount",
                "balance_amount",
                "status",
                "updated_at",
            ),
        )

        locked_claim.status = ClaimStatus.SETTLED
        locked_claim.settled_at = timezone.now()
        locked_claim.full_clean()
        locked_claim.save(
            update_fields=(
                "status",
                "settled_at",
                "updated_at",
            ),
        )

        return locked_claim


__all__ = ("InsuranceClaimService",)

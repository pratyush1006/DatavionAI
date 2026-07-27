"""
Insurance claim services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.billing.constants import (
    ClaimStatus,
    InvoiceStatus,
)
from apps.billing.models import InsuranceClaim


class InsuranceClaimService:
    """
    Application service responsible for insurance claim write operations.

    This service is the single entry point for all insurance claim
    lifecycle operations and provides a centralized location for
    future business rules such as:

    - Claim validation
    - Approval amount tracking
    - Settlement processing
    - Audit logging
    - Notifications
    - External integrations
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any = None,
    ) -> InsuranceClaim:
        """
        Create a new insurance claim.
        """

        claim = InsuranceClaim(
            **validated_data,
        )

        claim.full_clean()

        claim.save()

        return claim

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: InsuranceClaim,
        validated_data: Mapping[str, Any],
        performed_by: Any = None,
    ) -> InsuranceClaim:
        """
        Update an existing insurance claim.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def approve(
        *,
        instance: InsuranceClaim,
        approved_amount: float,
        performed_by: Any = None,
    ) -> InsuranceClaim:
        """
        Approve an insurance claim.
        """

        instance.approved_amount = approved_amount

        if approved_amount >= instance.claim_amount:
            instance.status = ClaimStatus.APPROVED
        else:
            instance.status = ClaimStatus.PARTIALLY_APPROVED

        instance.full_clean()

        instance.save(
            update_fields=[
                "approved_amount",
                "status",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def reject(
        *,
        instance: InsuranceClaim,
        rejection_reason: str,
        performed_by: Any = None,
    ) -> InsuranceClaim:
        """
        Reject an insurance claim.
        """

        instance.status = ClaimStatus.REJECTED
        instance.rejection_reason = rejection_reason

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "rejection_reason",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def appeal(
        *,
        instance: InsuranceClaim,
        performed_by: Any = None,
    ) -> InsuranceClaim:
        """
        Appeal a rejected insurance claim.
        """

        instance.status = ClaimStatus.APPEALED

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def settle(
        *,
        instance: InsuranceClaim,
        performed_by: Any = None,
    ) -> InsuranceClaim:
        """
        Settle an approved insurance claim.
        """

        from django.utils import timezone

        instance.status = ClaimStatus.SETTLED
        instance.settled_at = timezone.now()

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "settled_at",
            ],
        )

        invoice = instance.invoice

        if instance.approved_amount:
            remaining = invoice.balance_amount

            if instance.approved_amount >= remaining:
                invoice.status = InvoiceStatus.PAID
                invoice.balance_amount = 0
                invoice.paid_amount = invoice.total_amount
            else:
                invoice.paid_amount = invoice.paid_amount + instance.approved_amount
                invoice.balance_amount = invoice.total_amount - invoice.paid_amount

                if invoice.paid_amount > 0:
                    invoice.status = InvoiceStatus.PARTIALLY_PAID

            invoice.save(
                update_fields=[
                    "status",
                    "paid_amount",
                    "balance_amount",
                ],
            )

        return instance

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: Any = None,
    ) -> list[InsuranceClaim]:
        """
        Create multiple insurance claims.
        """

        claims: list[InsuranceClaim] = []

        for validated_data in validated_data_list:
            claim = InsuranceClaim(
                **validated_data,
            )

            claim.full_clean()

            claim.save()

            claims.append(claim)

        return claims


create_claim = InsuranceClaimService.create
approve_claim = InsuranceClaimService.approve
reject_claim = InsuranceClaimService.reject
appeal_claim = InsuranceClaimService.appeal
settle_claim = InsuranceClaimService.settle
update_claim = InsuranceClaimService.update


__all__ = [
    "InsuranceClaimService",
    "appeal_claim",
    "approve_claim",
    "create_claim",
    "reject_claim",
    "settle_claim",
]

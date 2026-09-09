"""Transactional services for Revenue Cycle Accounts Receivable."""

from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from apps.patient_management.patients.models import Patient

from .constants import (
    ARAccountStatus,
    ARAction,
    ARHoldReason,
    ARTransactionStatus,
    ARTransactionType,
)
from .events import publish_ar_event
from .models import ARAccount, ARActivityLog, ARTransaction


class ARService:
    """Perform concurrency-safe Accounts Receivable mutations."""

    @staticmethod
    def _audit(
        *,
        account: ARAccount,
        action: str,
        actor: Any,
        details: dict[str, Any],
    ) -> None:
        """Create an immutable AR activity record."""

        ARActivityLog.objects.create(
            organization_id=account.organization_id,
            account=account,
            action=action,
            details=details,
            performed_by=actor,
        )

    @staticmethod
    def _lock_account(
        *,
        organization_id: UUID,
        account_id: UUID,
    ) -> ARAccount:
        """Lock and return an AR account inside a transaction."""

        return ARAccount.objects.select_for_update().get(
            organization_id=organization_id,
            id=account_id,
        )

    @staticmethod
    def create_account(
        *,
        organization: Any,
        patient: Patient,
        account_number: str,
        currency: str,
        actor: Any,
    ) -> ARAccount:
        """Create a patient AR account after validating organization ownership."""

        if patient.organization_id != organization.id:
            raise ValueError("Patient does not belong to the organization.")

        account = ARAccount.objects.create(
            organization=organization,
            patient=patient,
            account_number=account_number,
            currency=currency,
        )
        ARService._audit(
            account=account,
            action=ARAction.CREATE,
            actor=actor,
            details={"account_number": account.account_number},
        )
        publish_ar_event(
            event_type="revenue_cycle.ar.account_created",
            aggregate_id=account.id,
            payload={
                "organization_id": str(organization.id),
                "patient_id": str(patient.id),
                "account_number": account.account_number,
            },
        )
        return account

    @staticmethod
    @transaction.atomic
    def post_transaction(
        *,
        organization: Any,
        account_id: UUID,
        transaction_type: str,
        amount: Decimal,
        transaction_number: str,
        transaction_date: Any,
        actor: Any,
        source_type: str = "",
        source_id: UUID | None = None,
        external_reference: str = "",
        note: str = "",
    ) -> ARTransaction:
        """Post a financial transaction while locking the account balance."""

        if amount <= Decimal("0.00"):
            raise ValueError("Transaction amount must be greater than zero.")

        account = ARService._lock_account(
            organization_id=organization.id,
            account_id=account_id,
        )

        if account.status in {
            ARAccountStatus.CLOSED,
            ARAccountStatus.WRITTEN_OFF,
        }:
            raise ValueError("Transactions cannot be posted to this account.")

        if transaction_type not in ARTransactionType.values:
            raise ValueError("Unsupported Accounts Receivable transaction type.")

        if (
            transaction_type
            in {
                ARTransactionType.PAYMENT,
                ARTransactionType.REFUND,
                ARTransactionType.ADJUSTMENT,
                ARTransactionType.DENIAL,
                ARTransactionType.WRITE_OFF,
            }
            and amount > account.balance_amount
        ):
            raise ValueError("Transaction exceeds the outstanding AR balance.")

        ar_transaction = ARTransaction.objects.create(
            organization=organization,
            account=account,
            patient=account.patient,
            transaction_number=transaction_number,
            transaction_type=transaction_type,
            amount=amount,
            transaction_date=transaction_date,
            source_type=source_type,
            source_id=source_id,
            external_reference=external_reference,
            note=note,
        )

        if transaction_type == ARTransactionType.CHARGE:
            account.total_charges += amount
            account.balance_amount += amount
        elif transaction_type == ARTransactionType.PAYMENT:
            account.total_payments += amount
            account.balance_amount -= amount
        elif transaction_type == ARTransactionType.ADJUSTMENT:
            account.total_adjustments += amount
            account.balance_amount -= amount
        elif transaction_type == ARTransactionType.DENIAL:
            account.balance_amount += amount
        elif transaction_type == ARTransactionType.WRITE_OFF:
            account.total_write_offs += amount
            account.balance_amount -= amount
        elif transaction_type == ARTransactionType.REFUND:
            account.total_payments -= amount
            account.balance_amount += amount

        account.version += 1
        if account.balance_amount == Decimal("0.00"):
            account.status = ARAccountStatus.PAID
        elif account.status == ARAccountStatus.PAID:
            account.status = ARAccountStatus.OPEN
        account.save(
            update_fields=[
                "total_charges",
                "total_payments",
                "total_adjustments",
                "total_write_offs",
                "balance_amount",
                "status",
                "version",
                "updated_at",
            ]
        )

        ARService._audit(
            account=account,
            action=ARAction.POST,
            actor=actor,
            details={
                "transaction_id": str(ar_transaction.id),
                "transaction_type": transaction_type,
                "amount": str(amount),
            },
        )
        publish_ar_event(
            event_type="revenue_cycle.ar.transaction_posted",
            aggregate_id=ar_transaction.id,
            payload={
                "organization_id": str(organization.id),
                "account_id": str(account.id),
                "patient_id": str(account.patient_id),
                "transaction_type": transaction_type,
                "amount": str(amount),
            },
        )
        return ar_transaction

    @staticmethod
    @transaction.atomic
    def reverse_transaction(
        *,
        organization: Any,
        transaction_id: UUID,
        actor: Any,
    ) -> ARTransaction:
        """Reverse a posted transaction with a compensating balance movement."""

        ar_transaction = (
            ARTransaction.objects.select_for_update()
            .select_related("account")
            .get(
                organization_id=organization.id,
                id=transaction_id,
            )
        )

        if ar_transaction.status != ARTransactionStatus.POSTED:
            raise ValueError("Only posted transactions can be reversed.")

        account = ARService._lock_account(
            organization_id=organization.id,
            account_id=ar_transaction.account_id,
        )

        amount = ar_transaction.amount
        transaction_type = ar_transaction.transaction_type

        if transaction_type == ARTransactionType.CHARGE:
            if account.balance_amount < amount:
                raise ValueError("Cannot reverse a charge below zero balance.")
            account.total_charges -= amount
            account.balance_amount -= amount
        elif transaction_type == ARTransactionType.PAYMENT:
            account.total_payments -= amount
            account.balance_amount += amount
        elif transaction_type == ARTransactionType.ADJUSTMENT:
            account.total_adjustments -= amount
            account.balance_amount += amount
        elif transaction_type == ARTransactionType.DENIAL:
            if account.balance_amount < amount:
                raise ValueError("Cannot reverse a denial below zero balance.")
            account.balance_amount -= amount
        elif transaction_type == ARTransactionType.WRITE_OFF:
            account.total_write_offs -= amount
            account.balance_amount += amount
        elif transaction_type == ARTransactionType.REFUND:
            account.total_payments += amount
            account.balance_amount -= amount

        ar_transaction.status = ARTransactionStatus.REVERSED
        ar_transaction.reversed_at = timezone.now()
        ar_transaction.reversed_by = actor
        ar_transaction.save(
            update_fields=[
                "status",
                "reversed_at",
                "reversed_by",
                "updated_at",
            ]
        )

        account.version += 1
        account.status = (
            ARAccountStatus.PAID
            if account.balance_amount == Decimal("0.00")
            else ARAccountStatus.OPEN
        )
        account.save(
            update_fields=["balance_amount", "status", "version", "updated_at"]
        )

        ARService._audit(
            account=account,
            action=ARAction.REVERSE,
            actor=actor,
            details={"transaction_id": str(ar_transaction.id)},
        )
        publish_ar_event(
            event_type="revenue_cycle.ar.transaction_reversed",
            aggregate_id=ar_transaction.id,
            payload={
                "organization_id": str(organization.id),
                "account_id": str(account.id),
                "amount": str(amount),
            },
        )
        return ar_transaction

    @staticmethod
    @transaction.atomic
    def set_hold(
        *,
        organization: Any,
        account_id: UUID,
        reason: str,
        note: str,
        actor: Any,
    ) -> ARAccount:
        """Place an AR account on hold."""

        if reason not in ARHoldReason.values:
            raise ValueError("Unsupported AR hold reason.")

        account = ARService._lock_account(
            organization_id=organization.id,
            account_id=account_id,
        )
        if account.status in {ARAccountStatus.CLOSED, ARAccountStatus.WRITTEN_OFF}:
            raise ValueError("Closed or written-off accounts cannot be held.")

        account.status = ARAccountStatus.ON_HOLD
        account.hold_reason = reason
        account.hold_note = note
        account.version += 1
        account.save(
            update_fields=[
                "status",
                "hold_reason",
                "hold_note",
                "version",
                "updated_at",
            ]
        )
        ARService._audit(
            account=account,
            action=ARAction.HOLD,
            actor=actor,
            details={"reason": reason},
        )
        publish_ar_event(
            event_type="revenue_cycle.ar.account_hold",
            aggregate_id=account.id,
            payload={"organization_id": str(organization.id), "reason": reason},
        )
        return account

    @staticmethod
    @transaction.atomic
    def release_hold(
        *,
        organization: Any,
        account_id: UUID,
        actor: Any,
    ) -> ARAccount:
        """Release an AR account hold."""

        account = ARService._lock_account(
            organization_id=organization.id,
            account_id=account_id,
        )
        if account.status != ARAccountStatus.ON_HOLD:
            raise ValueError("Account is not on hold.")

        account.status = (
            ARAccountStatus.PAID
            if account.balance_amount == Decimal("0.00")
            else ARAccountStatus.OPEN
        )
        account.hold_reason = ""
        account.hold_note = ""
        account.version += 1
        account.save(
            update_fields=[
                "status",
                "hold_reason",
                "hold_note",
                "version",
                "updated_at",
            ]
        )
        ARService._audit(
            account=account,
            action=ARAction.RELEASE_HOLD,
            actor=actor,
            details={},
        )
        publish_ar_event(
            event_type="revenue_cycle.ar.account_hold_released",
            aggregate_id=account.id,
            payload={"organization_id": str(organization.id)},
        )
        return account

    @staticmethod
    @transaction.atomic
    def write_off(
        *,
        organization: Any,
        account_id: UUID,
        actor: Any,
        transaction_number: str,
        note: str = "",
    ) -> ARTransaction:
        """Write off the complete current outstanding balance."""

        account = ARService._lock_account(
            organization_id=organization.id,
            account_id=account_id,
        )
        if account.balance_amount <= Decimal("0.00"):
            raise ValueError("There is no outstanding balance to write off.")

        amount = account.balance_amount
        return ARService.post_transaction(
            organization=organization,
            account_id=account.id,
            transaction_type=ARTransactionType.WRITE_OFF,
            amount=amount,
            transaction_number=transaction_number,
            transaction_date=timezone.now(),
            actor=actor,
            note=note,
        )


__all__ = ("ARService",)

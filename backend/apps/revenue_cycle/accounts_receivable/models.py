"""Persistent models for Revenue Cycle Accounts Receivable."""

from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient

from .constants import (
    ARAccountStatus,
    ARHoldReason,
    ARTransactionStatus,
    ARTransactionType,
)


class ARAccount(BaseModel):
    """Track the receivable balance for one patient and organization."""

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_ar_accounts",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_ar_accounts",
    )
    account_number = models.CharField(max_length=40)
    currency = models.CharField(max_length=3, default="INR")
    status = models.CharField(
        max_length=20,
        choices=ARAccountStatus.choices,
        default=ARAccountStatus.OPEN,
        db_index=True,
    )
    balance_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_charges = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_payments = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_adjustments = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_write_offs = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    hold_reason = models.CharField(
        max_length=30,
        choices=ARHoldReason.choices,
        blank=True,
    )
    hold_note = models.TextField(blank=True)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    version = models.PositiveBigIntegerField(default=1)

    class Meta:
        """Configure database constraints and indexes."""

        db_table = "revenue_cycle_ar_accounts"
        ordering = ("-created_at",)
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "account_number"),
                name="unique_rc_ar_account_number",
            ),
            models.CheckConstraint(
                condition=Q(balance_amount__gte=0),
                name="rc_ar_balance_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(total_charges__gte=0),
                name="rc_ar_charges_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(total_payments__gte=0),
                name="rc_ar_payments_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(total_adjustments__gte=0),
                name="rc_ar_adjustments_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(total_write_offs__gte=0),
                name="rc_ar_writeoffs_non_negative",
            ),
        )
        indexes = (
            models.Index(
                fields=("organization", "patient", "status"),
                name="rc_ar_org_patient_status_idx",
            ),
            models.Index(
                fields=("organization", "balance_amount"),
                name="rc_ar_org_balance_idx",
            ),
        )

    def __str__(self) -> str:
        """Return the account number."""

        return self.account_number


class ARTransaction(BaseModel):
    """Record an immutable financial movement against an AR account."""

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_ar_transactions",
    )
    account = models.ForeignKey(
        ARAccount,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_ar_transactions",
    )
    transaction_number = models.CharField(max_length=50)
    transaction_type = models.CharField(
        max_length=20,
        choices=ARTransactionType.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=ARTransactionStatus.choices,
        default=ARTransactionStatus.POSTED,
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )
    transaction_date = models.DateTimeField()
    source_type = models.CharField(max_length=50, blank=True)
    source_id = models.UUIDField(null=True, blank=True)
    external_reference = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)
    reversed_at = models.DateTimeField(null=True, blank=True)
    reversed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reversed_rc_ar_transactions",
    )

    class Meta:
        """Configure transaction uniqueness and indexes."""

        db_table = "revenue_cycle_ar_transactions"
        ordering = ("-transaction_date", "-created_at")
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "transaction_number"),
                name="unique_rc_ar_transaction_number",
            ),
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="rc_ar_transaction_amount_positive",
            ),
        )
        indexes = (
            models.Index(
                fields=("organization", "account", "transaction_date"),
                name="rc_ar_account_date_idx",
            ),
            models.Index(
                fields=("organization", "patient", "transaction_date"),
                name="rc_ar_patient_date_idx",
            ),
            models.Index(
                fields=("organization", "transaction_type", "status"),
                name="rc_ar_type_status_idx",
            ),
        )

    def __str__(self) -> str:
        """Return the transaction number."""

        return self.transaction_number


class ARActivityLog(BaseModel):
    """Store an immutable audit trail for AR lifecycle actions."""

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_ar_activity_logs",
    )
    account = models.ForeignKey(
        ARAccount,
        on_delete=models.PROTECT,
        related_name="activity_logs",
    )
    action = models.CharField(max_length=30)
    details = models.JSONField(default=dict, blank=True)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revenue_cycle_ar_activity_logs",
    )
    performed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Configure audit ordering and indexes."""

        db_table = "revenue_cycle_ar_activity_logs"
        ordering = ("-performed_at",)
        indexes = (
            models.Index(
                fields=("organization", "account", "performed_at"),
                name="rc_ar_activity_idx",
            ),
        )


__all__ = ("ARAccount", "ARTransaction", "ARActivityLog")

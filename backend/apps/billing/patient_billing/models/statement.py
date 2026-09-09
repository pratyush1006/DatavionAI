"""Patient billing statement model."""

from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.billing.patient_billing.constants import PatientStatementStatus
from apps.core.models import BaseModel


class PatientBillingStatement(BaseModel):
    """Immutable-period financial statement summarizing patient activity."""

    account = models.ForeignKey(
        "billing.PatientBillingAccount",
        on_delete=models.PROTECT,
        related_name="statements",
    )
    statement_number = models.CharField(
        max_length=60,
        db_index=True,
    )
    period_start = models.DateField()
    period_end = models.DateField()
    opening_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    charges = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    payments = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    adjustments = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    closing_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    status = models.CharField(
        max_length=20,
        choices=PatientStatementStatus.choices,
        default=PatientStatementStatus.DRAFT,
        db_index=True,
    )
    issued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        """Database metadata."""

        db_table = "billing_patient_statements"
        ordering = ("-period_end", "-created_at")
        constraints = (
            models.UniqueConstraint(
                fields=("account", "statement_number"),
                name="unique_patient_statement_number",
            ),
            models.UniqueConstraint(
                fields=("account", "period_start", "period_end"),
                name="unique_patient_statement_period",
            ),
            models.CheckConstraint(
                condition=models.Q(period_end__gte=models.F("period_start")),
                name="patient_statement_valid_period",
            ),
        )
        indexes = (
            models.Index(
                fields=("account", "period_end"),
                name="pstmt_account_end_idx",
            ),
            models.Index(
                fields=("account", "status"),
                name="pstmt_account_status_idx",
            ),
        )

    def __str__(self) -> str:
        """Return the statement number."""

        return self.statement_number


__all__ = ("PatientBillingStatement",)

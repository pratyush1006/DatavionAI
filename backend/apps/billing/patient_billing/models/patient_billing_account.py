"""
Patient billing account model.

Defines the financial account associated with a canonical patient
within a billing organization.
"""

from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.billing.foundation.currency import SUPPORTED_CURRENCIES
from apps.billing.patient_billing.constants import PatientBillingAccountStatus
from apps.core.models import BaseModel


class PatientBillingAccount(BaseModel):
    """
    Financial account anchoring a patient's billing relationship.

    Currency availability is sourced from the Billing Foundation so that
    Patient Billing does not maintain a second currency registry.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="patient_billing_accounts",
    )

    patient = models.OneToOneField(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="billing_account",
    )

    account_number = models.CharField(
        max_length=50,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=PatientBillingAccountStatus.choices,
        default=PatientBillingAccountStatus.ACTIVE,
        db_index=True,
    )

    currency = models.CharField(
        max_length=3,
        choices=tuple(
            (currency_code, currency_code) for currency_code in SUPPORTED_CURRENCIES
        ),
        default="INR",
    )

    opening_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(
                Decimal("0.00"),
            ),
        ],
    )

    credit_limit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(
                Decimal("0.00"),
            ),
        ],
    )

    current_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    notes = models.TextField(
        blank=True,
        default="",
    )

    class Meta:
        """Database metadata."""

        db_table = "billing_patient_accounts"

        ordering = ("account_number",)

        constraints = (
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "account_number",
                ),
                name="unique_patient_billing_account_number",
            ),
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "patient",
                ),
                name="unique_patient_billing_account_patient",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    opening_balance__gte=Decimal("0.00"),
                ),
                name="patient_billing_opening_balance_nonnegative",
            ),
        )

        indexes = (
            models.Index(
                fields=(
                    "organization",
                    "status",
                ),
                name="pba_org_status_idx",
            ),
            models.Index(
                fields=(
                    "organization",
                    "patient",
                ),
                name="pba_org_patient_idx",
            ),
        )

    def __str__(self) -> str:
        """
        Return the billing account number.
        """

        return self.account_number


__all__ = ("PatientBillingAccount",)

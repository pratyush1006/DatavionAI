"""Patient financial responsibility model."""

from __future__ import annotations

from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.billing.patient_billing.constants import BillingPartyType
from apps.billing.patient_billing.models.guarantor import PatientGuarantor
from apps.core.models import BaseModel


class PatientFinancialResponsibility(BaseModel):
    """Defines how financial responsibility is assigned for a patient account."""

    account = models.ForeignKey(
        "billing.PatientBillingAccount",
        on_delete=models.PROTECT,
        related_name="responsibilities",
    )
    party_type = models.CharField(max_length=20, choices=BillingPartyType.choices)
    guarantor = models.ForeignKey(
        PatientGuarantor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="responsibilities",
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("100.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ],
    )
    priority = models.PositiveIntegerField(default=1)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        """Database metadata."""

        db_table = "billing_patient_responsibilities"
        ordering = ("priority", "effective_from")
        indexes = (
            models.Index(
                fields=("account", "party_type"), name="presp_account_party_idx"
            ),
            models.Index(
                fields=("account", "effective_from"), name="presp_account_date_idx"
            ),
        )

    def clean(self) -> None:
        """Validate guarantor requirements and date ordering."""

        super().clean()
        if self.party_type == BillingPartyType.GUARANTOR and self.guarantor_id is None:
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {"guarantor": "A guarantor is required for GUARANTOR responsibility."}
            )
        if (
            self.party_type != BillingPartyType.GUARANTOR
            and self.guarantor_id is not None
        ):
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {"guarantor": "Guarantor is only valid for GUARANTOR responsibility."}
            )
        if self.effective_to and self.effective_to < self.effective_from:
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {"effective_to": "effective_to cannot precede effective_from."}
            )

    def __str__(self) -> str:
        """Return the responsibility display value."""

        return f"{self.account.account_number} - {self.party_type}"


__all__ = ("PatientFinancialResponsibility",)

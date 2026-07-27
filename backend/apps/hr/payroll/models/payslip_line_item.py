from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.payroll.models.payslip import Payslip


class PayslipLineItemType(models.TextChoices):
    """
    Whether a payslip line item adds to or subtracts from pay.
    """

    EARNING = "earning", "Earning"
    DEDUCTION = "deduction", "Deduction"


class PayslipLineItem(TimeStampedModel):
    """
    Represents a single earning or deduction line on a payslip,
    e.g. "Overtime Pay" or "Income Tax".
    """

    payslip = models.ForeignKey(
        Payslip,
        on_delete=models.CASCADE,
        related_name="line_items",
    )

    component_type = models.CharField(
        max_length=20,
        choices=PayslipLineItemType.choices,
    )

    name = models.CharField(
        max_length=100,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        ordering = [
            "component_type",
            "name",
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the payslip line item display name.
        """

        return f"{self.payslip} - {self.name}"


__all__ = [
    "PayslipLineItemType",
    "PayslipLineItem",
]

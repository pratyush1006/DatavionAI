from decimal import Decimal

from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import BillingStatus
from apps.pharmacy.models.dispensing import DispensingOrder


class PharmacyBillingRecord(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_billing_records",
    )
    dispensing_order = models.OneToOneField(
        DispensingOrder, on_delete=models.PROTECT, related_name="billing_record"
    )
    currency = models.CharField(max_length=3, default="INR")
    subtotal = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0")
    )
    tax_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0")
    )
    total_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0")
    )
    status = models.CharField(
        max_length=20, choices=BillingStatus.choices, default=BillingStatus.PENDING
    )
    external_invoice_id = models.CharField(max_length=120, blank=True)

    class Meta:
        db_table = "pharmacy_billing_records"
        indexes = [models.Index(fields=("organization", "status"))]

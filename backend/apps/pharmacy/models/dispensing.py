from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import DispenseStatus
from apps.pharmacy.models.batch import MedicationBatch
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.models.product import PharmacyProduct


class DispensingOrder(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_dispensing_orders",
    )
    pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.PROTECT, related_name="dispensing_orders"
    )
    prescription = models.ForeignKey(
        "prescriptions.Prescription",
        on_delete=models.PROTECT,
        related_name="pharmacy_dispensing_orders",
    )
    dispense_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=30, choices=DispenseStatus.choices, default=DispenseStatus.DRAFT
    )
    pharmacist_id = models.UUIDField(null=True, blank=True)
    dispensed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pharmacy_dispensing_orders"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "dispense_number"),
                name="unique_pharmacy_dispense_number",
            )
        ]


class DispensingLine(BaseModel):
    dispensing_order = models.ForeignKey(
        DispensingOrder, on_delete=models.CASCADE, related_name="lines"
    )
    product = models.ForeignKey(
        PharmacyProduct, on_delete=models.PROTECT, related_name="dispensing_lines"
    )
    batch = models.ForeignKey(
        MedicationBatch, on_delete=models.PROTECT, related_name="dispensing_lines"
    )
    quantity_prescribed = models.DecimalField(max_digits=14, decimal_places=3)
    quantity_dispensed = models.DecimalField(max_digits=14, decimal_places=3, default=0)

from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import ReturnType
from apps.pharmacy.models.batch import MedicationBatch
from apps.pharmacy.models.dispensing import DispensingOrder
from apps.pharmacy.models.product import PharmacyProduct
from apps.pharmacy.models.purchase import PurchaseOrder


class PharmacyReturn(BaseModel):
    return_type = models.CharField(max_length=20, choices=ReturnType.choices)
    dispensing_order = models.ForeignKey(
        DispensingOrder,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="returns",
    )
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="returns",
    )
    return_number = models.CharField(max_length=50)
    reason = models.TextField()
    processed_by_id = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = "pharmacy_returns"
        constraints = [
            models.UniqueConstraint(
                fields=("return_number",),
                name="unique_pharmacy_return_number",
            )
        ]


class PharmacyReturnLine(BaseModel):
    pharmacy_return = models.ForeignKey(
        PharmacyReturn, on_delete=models.CASCADE, related_name="lines"
    )
    product = models.ForeignKey(
        PharmacyProduct, on_delete=models.PROTECT, related_name="return_lines"
    )
    batch = models.ForeignKey(
        MedicationBatch, on_delete=models.PROTECT, related_name="return_lines"
    )
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    restockable = models.BooleanField(default=False)

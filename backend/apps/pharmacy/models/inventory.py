from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import StockMovementType
from apps.pharmacy.models.batch import MedicationBatch


class StockMovement(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_stock_movements",
    )
    batch = models.ForeignKey(
        MedicationBatch, on_delete=models.PROTECT, related_name="stock_movements"
    )
    movement_type = models.CharField(max_length=30, choices=StockMovementType.choices)
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    reference_type = models.CharField(max_length=80, blank=True)
    reference_id = models.UUIDField(null=True, blank=True)
    actor_id = models.UUIDField(null=True, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "pharmacy_stock_movements"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("organization", "created_at")),
            models.Index(fields=("batch", "created_at")),
        ]

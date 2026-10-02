from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import QuarantineStatus
from apps.pharmacy.models.batch import MedicationBatch


class InventoryQuarantine(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_quarantines",
    )
    batch = models.ForeignKey(
        MedicationBatch, on_delete=models.PROTECT, related_name="quarantine_records"
    )
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=QuarantineStatus.choices,
        default=QuarantineStatus.QUARANTINED,
    )
    quarantined_by_id = models.UUIDField(null=True, blank=True)
    released_by_id = models.UUIDField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pharmacy_inventory_quarantines"
        indexes = [
            models.Index(fields=("organization", "status")),
            models.Index(fields=("batch", "status")),
        ]

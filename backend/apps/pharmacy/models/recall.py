from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import RecallStatus
from apps.pharmacy.models.batch import MedicationBatch
from apps.pharmacy.models.product import PharmacyProduct


class ProductRecall(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_recalls",
    )
    product = models.ForeignKey(
        PharmacyProduct, on_delete=models.PROTECT, related_name="recalls"
    )
    recall_number = models.CharField(max_length=80)
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=RecallStatus.choices, default=RecallStatus.OPEN
    )
    initiated_by_id = models.UUIDField(null=True, blank=True)
    initiated_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pharmacy_product_recalls"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "recall_number"),
                name="unique_pharmacy_recall_number",
            )
        ]


class RecallBatch(BaseModel):
    recall = models.ForeignKey(
        ProductRecall, on_delete=models.CASCADE, related_name="batches"
    )
    batch = models.ForeignKey(
        MedicationBatch, on_delete=models.PROTECT, related_name="recalls"
    )
    quantity_affected = models.DecimalField(max_digits=14, decimal_places=3)
    quarantined = models.BooleanField(default=False)

    class Meta:
        db_table = "pharmacy_recall_batches"
        constraints = [
            models.UniqueConstraint(
                fields=("recall", "batch"), name="unique_recall_batch"
            )
        ]

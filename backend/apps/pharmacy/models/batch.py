from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.models.product import PharmacyProduct


class MedicationBatch(BaseModel):
    product = models.ForeignKey(
        PharmacyProduct, on_delete=models.PROTECT, related_name="batches"
    )
    batch_number = models.CharField(max_length=100)
    manufacture_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField()
    quantity_received = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    quantity_available = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    quantity_reserved = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    purchase_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = "pharmacy_medication_batches"
        constraints = [
            models.UniqueConstraint(
                fields=("product", "batch_number"),
                name="unique_batch_per_pharmacy_product",
            )
        ]
        indexes = [
            models.Index(fields=("expiry_date",)),
            models.Index(fields=("product", "expiry_date")),
        ]

    @property
    def is_expired(self):
        from django.utils import timezone

        return self.expiry_date < timezone.localdate()

    def __str__(self):
        return f"{self.product.sku} | {self.batch_number}"

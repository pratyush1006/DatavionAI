from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.models.pharmacy import Pharmacy


class PharmacyProduct(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="pharmacy_products",
    )
    pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.CASCADE, related_name="products"
    )
    medication = models.ForeignKey(
        "medications.Medication",
        on_delete=models.PROTECT,
        related_name="pharmacy_products",
    )
    sku = models.CharField(max_length=80)
    barcode = models.CharField(max_length=100, blank=True)
    reorder_level = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    reorder_quantity = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    unit_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=7, decimal_places=3, default=0)

    class Meta:
        db_table = "pharmacy_products"
        constraints = [
            models.UniqueConstraint(
                fields=("pharmacy", "sku"),
                name="unique_pharmacy_product_sku",
            )
        ]
        indexes = [
            models.Index(fields=("pharmacy", "medication")),
            models.Index(fields=("barcode",)),
        ]

    def __str__(self):
        return f"{self.sku} | {self.medication}"

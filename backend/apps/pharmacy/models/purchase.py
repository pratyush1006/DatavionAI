from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import PurchaseOrderStatus
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.models.product import PharmacyProduct
from apps.pharmacy.models.supplier import Supplier


class PurchaseOrder(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_purchase_orders",
    )
    pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.PROTECT, related_name="purchase_orders"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="purchase_orders"
    )
    order_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=30,
        choices=PurchaseOrderStatus.choices,
        default=PurchaseOrderStatus.DRAFT,
    )
    ordered_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "pharmacy_purchase_orders"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "order_number"),
                name="unique_pharmacy_purchase_order_number",
            )
        ]


class PurchaseOrderLine(BaseModel):
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="lines"
    )
    product = models.ForeignKey(
        PharmacyProduct, on_delete=models.PROTECT, related_name="purchase_lines"
    )
    quantity_ordered = models.DecimalField(max_digits=14, decimal_places=3)
    quantity_received = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    unit_cost = models.DecimalField(max_digits=14, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=7, decimal_places=3, default=0)

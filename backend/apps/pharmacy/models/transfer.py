from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import TransferOrderStatus
from apps.pharmacy.models.batch import MedicationBatch
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.models.product import PharmacyProduct


class StockTransferOrder(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="pharmacy_transfer_orders",
    )
    source_pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.PROTECT, related_name="outbound_transfer_orders"
    )
    destination_pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.PROTECT, related_name="inbound_transfer_orders"
    )
    transfer_number = models.CharField(max_length=80)
    status = models.CharField(
        max_length=20,
        choices=TransferOrderStatus.choices,
        default=TransferOrderStatus.DRAFT,
    )
    approved_by_id = models.UUIDField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pharmacy_stock_transfer_orders"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "transfer_number"),
                name="unique_pharmacy_transfer_number",
            ),
        ]


class StockTransferLine(BaseModel):
    transfer_order = models.ForeignKey(
        StockTransferOrder, on_delete=models.CASCADE, related_name="lines"
    )
    source_batch = models.ForeignKey(
        MedicationBatch,
        on_delete=models.PROTECT,
        related_name="outbound_transfer_lines",
    )
    destination_product = models.ForeignKey(
        PharmacyProduct, on_delete=models.PROTECT, related_name="inbound_transfer_lines"
    )
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    destination_batch = models.ForeignKey(
        MedicationBatch,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="destination_transfer_lines",
    )

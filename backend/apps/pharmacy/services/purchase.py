from decimal import Decimal

from django.db import models, transaction

from apps.pharmacy.constants import PurchaseOrderStatus
from apps.pharmacy.models import PurchaseOrder, PurchaseOrderLine


@transaction.atomic
def create_purchase_order(
    *, organization, pharmacy, supplier, order_number, lines, actor=None
):
    if pharmacy.organization_id != organization.id:
        raise ValueError("Pharmacy does not belong to the organization.")
    if supplier.organization_id != organization.id:
        raise ValueError("Supplier does not belong to the organization.")
    order = PurchaseOrder.objects.create(
        organization=organization,
        pharmacy=pharmacy,
        supplier=supplier,
        order_number=order_number,
    )
    for item in lines:
        product = item["product"]
        if (
            product.organization_id != organization.id
            or product.pharmacy_id != pharmacy.id
        ):
            raise ValueError("Purchase product is outside the pharmacy scope.")
        PurchaseOrderLine.objects.create(purchase_order=order, **item)
    return order


@transaction.atomic
def receive_purchase_order(*, organization, purchase_order, receipts, actor_id=None):
    """Receive purchase lines atomically and create/update traceable batches."""
    from django.utils import timezone

    from apps.pharmacy.models import MedicationBatch
    from apps.pharmacy.services.inventory import receive_stock

    if purchase_order.organization_id != organization.id:
        raise ValueError("Purchase order is outside the organization scope.")
    if purchase_order.status == "cancelled":
        raise ValueError("Cancelled purchase orders cannot be received.")
    received_any = False
    for receipt in receipts:
        line = (
            purchase_order.lines.select_for_update()
            .filter(pk=receipt["line_id"])
            .first()
        )
        if line is None:
            raise ValueError("Purchase order line not found.")
        quantity = Decimal(str(receipt["quantity"]))
        if quantity <= 0:
            raise ValueError("Received quantity must be greater than zero.")
        if line.quantity_received + quantity > line.quantity_ordered:
            raise ValueError("Received quantity exceeds ordered quantity.")
        batch, _ = MedicationBatch.objects.get_or_create(
            product=line.product,
            batch_number=receipt["batch_number"],
            defaults={
                "manufacture_date": receipt.get("manufacture_date"),
                "expiry_date": receipt["expiry_date"],
                "purchase_price": line.unit_cost,
                "selling_price": line.product.selling_price,
            },
        )
        if batch.expiry_date < timezone.localdate():
            raise ValueError(
                "Expired stock cannot be received into available inventory."
            )
        receive_stock(
            organization=organization,
            batch=batch,
            quantity=quantity,
            actor_id=actor_id,
            reference_id=purchase_order.id,
        )
        line.quantity_received += quantity
        line.save(update_fields=["quantity_received", "updated_at"])
        received_any = True
    if received_any:
        remaining = purchase_order.lines.filter(
            quantity_received__lt=models.F("quantity_ordered")
        ).exists()
        purchase_order.status = (
            PurchaseOrderStatus.PARTIALLY_RECEIVED
            if remaining
            else PurchaseOrderStatus.RECEIVED
        )
        purchase_order.received_at = timezone.now()
        purchase_order.save(update_fields=["status", "received_at", "updated_at"])
    return purchase_order

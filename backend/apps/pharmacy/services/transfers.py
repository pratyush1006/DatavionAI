from django.db import transaction
from django.utils import timezone

from apps.pharmacy.constants import TransferOrderStatus
from apps.pharmacy.models import MedicationBatch, StockTransferLine, StockTransferOrder
from apps.pharmacy.services.inventory import transfer_stock


@transaction.atomic
def create_transfer_order(
    *,
    organization,
    source_pharmacy,
    destination_pharmacy,
    transfer_number,
    lines,
    actor_id=None,
):
    if (
        source_pharmacy.organization_id != organization.id
        or destination_pharmacy.organization_id != organization.id
    ):
        raise ValueError("Both pharmacies must belong to the organization.")
    if source_pharmacy.id == destination_pharmacy.id:
        raise ValueError("Source and destination pharmacies must differ.")
    order = StockTransferOrder.objects.create(
        organization=organization,
        source_pharmacy=source_pharmacy,
        destination_pharmacy=destination_pharmacy,
        transfer_number=transfer_number,
        approved_by_id=actor_id,
        status=TransferOrderStatus.APPROVED,
    )
    for item in lines:
        source_batch = item["source_batch"]
        destination_product = item["destination_product"]
        if source_batch.product.pharmacy_id != source_pharmacy.id:
            raise ValueError("Source batch is outside the source pharmacy.")
        if destination_product.pharmacy_id != destination_pharmacy.id:
            raise ValueError("Destination product is outside the destination pharmacy.")
        if source_batch.product.medication_id != destination_product.medication_id:
            raise ValueError(
                "Source and destination products must reference the same medication."
            )
        StockTransferLine.objects.create(transfer_order=order, **item)
    return order


@transaction.atomic
def complete_transfer_order(*, organization, order, actor_id=None):
    order = (
        StockTransferOrder.objects.select_for_update()
        .prefetch_related("lines__source_batch__product", "lines__destination_product")
        .get(pk=order.pk)
    )
    if order.organization_id != organization.id:
        raise ValueError("Transfer order is outside the organization scope.")
    if order.status == TransferOrderStatus.COMPLETED:
        return order
    if order.status not in (
        TransferOrderStatus.APPROVED,
        TransferOrderStatus.IN_TRANSIT,
    ):
        raise ValueError("Transfer order cannot be completed in its current state.")
    for line in order.lines.all():
        source_batch = (
            MedicationBatch.objects.select_for_update()
            .select_related("product")
            .get(pk=line.source_batch_id)
        )
        destination_product = line.destination_product
        if (
            source_batch.product.pharmacy_id != order.source_pharmacy_id
            or destination_product.pharmacy_id != order.destination_pharmacy_id
        ):
            raise ValueError("Transfer line pharmacy scope is invalid.")
        if source_batch.product.medication_id != destination_product.medication_id:
            raise ValueError("Transfer line medication mismatch.")
        destination_batch = line.destination_batch
        if destination_batch is None:
            destination_batch, _ = MedicationBatch.objects.get_or_create(
                product=destination_product,
                batch_number=source_batch.batch_number,
                defaults={
                    "manufacture_date": source_batch.manufacture_date,
                    "expiry_date": source_batch.expiry_date,
                    "purchase_price": source_batch.purchase_price,
                    "selling_price": source_batch.selling_price,
                },
            )
        elif destination_batch.product_id != destination_product.id:
            raise ValueError(
                "Destination batch does not belong to destination product."
            )
        if destination_batch.expiry_date != source_batch.expiry_date:
            raise ValueError("Transferred batch expiry must remain unchanged.")
        transfer_stock(
            organization=organization,
            batch=source_batch,
            quantity=line.quantity,
            destination_batch=destination_batch,
            actor=actor_id,
            reference_type="stock_transfer",
            reference_id=order.id,
            note=order.transfer_number,
        )
        if line.destination_batch_id != destination_batch.id:
            line.destination_batch_id = destination_batch.id
            line.save(update_fields=["destination_batch", "updated_at"])
    order.status = TransferOrderStatus.COMPLETED
    order.completed_at = timezone.now()
    order.save(update_fields=["status", "completed_at", "updated_at"])
    return order

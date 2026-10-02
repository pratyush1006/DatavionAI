from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.pharmacy.constants import StockMovementType
from apps.pharmacy.models import MedicationBatch, StockMovement
from apps.pharmacy.services.events import enqueue_event


def _decimal(value):
    value = Decimal(str(value))
    if value <= 0:
        raise ValidationError("Quantity must be greater than zero.")
    return value


def _check_scope(batch, organization):
    if batch.product.organization_id != organization.id:
        raise ValidationError("Inventory item is outside the organization scope.")


@transaction.atomic
def receive_stock(
    *,
    organization,
    batch,
    quantity,
    actor=None,
    actor_id=None,
    reference_type="",
    reference_id=None,
    note="",
):
    quantity = _decimal(quantity)
    if actor is None:
        actor = actor_id
    batch = (
        MedicationBatch.objects.select_for_update()
        .select_related("product")
        .get(pk=batch.pk)
    )
    _check_scope(batch, organization)
    if batch.expiry_date < timezone.localdate():
        raise ValidationError("Expired medication batches cannot receive stock.")
    batch.quantity_received += quantity
    batch.quantity_available += quantity
    batch.save(update_fields=["quantity_received", "quantity_available", "updated_at"])
    movement = StockMovement.objects.create(
        organization=organization,
        batch=batch,
        movement_type=StockMovementType.RECEIPT,
        quantity=quantity,
        reference_type=reference_type,
        reference_id=reference_id,
        actor_id=getattr(actor, "pk", actor) if actor else None,
        note=note,
    )
    enqueue_event(
        organization=organization,
        event_type="pharmacy.stock_received",
        aggregate_type="MedicationBatch",
        aggregate_id=batch.id,
        payload={
            "batch_id": str(batch.id),
            "quantity": str(quantity),
            "movement_id": str(movement.id),
        },
    )
    return movement


@transaction.atomic
def dispense_stock(
    *,
    organization,
    batch,
    quantity,
    actor=None,
    reference_type="",
    reference_id=None,
    note="",
):
    quantity = _decimal(quantity)
    batch = (
        MedicationBatch.objects.select_for_update()
        .select_related("product")
        .get(pk=batch.pk)
    )
    _check_scope(batch, organization)
    if batch.expiry_date < timezone.localdate():
        raise ValidationError("Expired medication cannot be dispensed.")
    available = batch.quantity_available - batch.quantity_reserved
    if available < quantity:
        raise ValidationError("Insufficient available stock.")
    batch.quantity_available -= quantity
    batch.save(update_fields=["quantity_available", "updated_at"])
    movement = StockMovement.objects.create(
        organization=organization,
        batch=batch,
        movement_type=StockMovementType.DISPENSE,
        quantity=quantity,
        reference_type=reference_type,
        reference_id=reference_id,
        actor_id=getattr(actor, "pk", actor) if actor else None,
        note=note,
    )
    enqueue_event(
        organization=organization,
        event_type="pharmacy.stock_dispensed",
        aggregate_type="MedicationBatch",
        aggregate_id=batch.id,
        payload={
            "batch_id": str(batch.id),
            "quantity": str(quantity),
            "movement_id": str(movement.id),
        },
    )
    return movement


@transaction.atomic
def dispense_product(
    *,
    organization,
    product,
    quantity,
    actor=None,
    reference_type="",
    reference_id=None,
    note="",
):
    quantity = _decimal(quantity)
    if product.organization_id != organization.id:
        raise ValidationError("Product is outside the organization scope.")
    remaining = quantity
    movements = []
    today = timezone.localdate()
    batches = (
        MedicationBatch.objects.select_for_update()
        .filter(product=product, expiry_date__gte=today, quantity_available__gt=0)
        .order_by("expiry_date", "created_at", "id")
    )
    for batch in batches:
        available = batch.quantity_available - batch.quantity_reserved
        if available <= 0:
            continue
        take = min(available, remaining)
        batch.quantity_available -= take
        batch.save(update_fields=["quantity_available", "updated_at"])
        movement = StockMovement.objects.create(
            organization=organization,
            batch=batch,
            movement_type=StockMovementType.DISPENSE,
            quantity=take,
            reference_type=reference_type,
            reference_id=reference_id,
            actor_id=getattr(actor, "pk", actor) if actor else None,
            note=note,
        )
        movements.append(movement)
        enqueue_event(
            organization=organization,
            event_type="pharmacy.stock_dispensed",
            aggregate_type="MedicationBatch",
            aggregate_id=batch.id,
            payload={
                "batch_id": str(batch.id),
                "quantity": str(take),
                "movement_id": str(movement.id),
            },
        )
        remaining -= take
        if remaining <= 0:
            break
    if remaining > 0:
        raise ValidationError(
            "Insufficient available stock for the requested product quantity."
        )
    return movements


@transaction.atomic
def return_stock(
    *,
    organization,
    batch,
    quantity,
    restockable=False,
    actor=None,
    reference_type="",
    reference_id=None,
    note="",
):
    """Record a returned item and optionally restore it to available inventory.

    Returned medication is only added back to sellable/dispensable stock when
    the caller explicitly marks it as restockable. This prevents non-restockable
    patient returns from silently increasing inventory.
    """
    quantity = _decimal(quantity)
    batch = (
        MedicationBatch.objects.select_for_update()
        .select_related("product")
        .get(pk=batch.pk)
    )
    _check_scope(batch, organization)
    if restockable:
        if batch.expiry_date < timezone.localdate():
            raise ValidationError(
                "Expired medication cannot be returned to available stock."
            )
        batch.quantity_available += quantity
        batch.save(update_fields=["quantity_available", "updated_at"])
    movement = StockMovement.objects.create(
        organization=organization,
        batch=batch,
        movement_type=StockMovementType.PATIENT_RETURN,
        quantity=quantity,
        reference_type=reference_type,
        reference_id=reference_id,
        actor_id=getattr(actor, "pk", actor) if actor else None,
        note=note,
    )
    enqueue_event(
        organization=organization,
        event_type="pharmacy.stock_returned",
        aggregate_type="MedicationBatch",
        aggregate_id=batch.id,
        payload={
            "batch_id": str(batch.id),
            "quantity": str(quantity),
            "restockable": restockable,
            "movement_id": str(movement.id),
        },
    )
    return movement


@transaction.atomic
def adjust_stock(
    *,
    organization,
    batch,
    quantity_delta,
    actor=None,
    reference_type="",
    reference_id=None,
    note="",
):
    delta = Decimal(str(quantity_delta))
    if delta == 0:
        raise ValidationError("Adjustment quantity cannot be zero.")
    batch = (
        MedicationBatch.objects.select_for_update()
        .select_related("product")
        .get(pk=batch.pk)
    )
    _check_scope(batch, organization)
    new_available = batch.quantity_available + delta
    if new_available < 0:
        raise ValidationError("Stock adjustment cannot create negative stock.")
    batch.quantity_available = new_available
    batch.save(update_fields=["quantity_available", "updated_at"])
    return StockMovement.objects.create(
        organization=organization,
        batch=batch,
        movement_type=StockMovementType.ADJUSTMENT,
        quantity=abs(delta),
        reference_type=reference_type,
        reference_id=reference_id,
        actor_id=getattr(actor, "pk", actor) if actor else None,
        note=note,
    )


@transaction.atomic
def transfer_stock(
    *,
    organization,
    batch,
    quantity,
    destination_batch,
    actor=None,
    reference_type="",
    reference_id=None,
    note="",
):
    quantity = _decimal(quantity)
    batch = (
        MedicationBatch.objects.select_for_update()
        .select_related("product")
        .get(pk=batch.pk)
    )
    destination_batch = (
        MedicationBatch.objects.select_for_update()
        .select_related("product")
        .get(pk=destination_batch.pk)
    )
    _check_scope(batch, organization)
    _check_scope(destination_batch, organization)
    if batch.product.medication_id != destination_batch.product.medication_id:
        raise ValidationError("Stock transfers require the same medication.")
    if destination_batch.expiry_date < timezone.localdate():
        raise ValidationError("Cannot transfer stock into an expired batch.")
    available = batch.quantity_available - batch.quantity_reserved
    if available < quantity:
        raise ValidationError("Insufficient available stock for transfer.")
    batch.quantity_available -= quantity
    destination_batch.quantity_available += quantity
    batch.save(update_fields=["quantity_available", "updated_at"])
    destination_batch.save(update_fields=["quantity_available", "updated_at"])
    kwargs = dict(
        organization=organization,
        quantity=quantity,
        reference_type=reference_type,
        reference_id=reference_id,
        actor_id=getattr(actor, "pk", actor) if actor else None,
        note=note,
    )
    outbound = StockMovement.objects.create(
        batch=batch, movement_type=StockMovementType.TRANSFER_OUT, **kwargs
    )
    inbound = StockMovement.objects.create(
        batch=destination_batch, movement_type=StockMovementType.TRANSFER_IN, **kwargs
    )
    return outbound, inbound


def available_stock(*, organization, product):
    if product.organization_id != organization.id:
        raise ValidationError("Product is outside the organization scope.")
    return sum(
        (b.quantity_available - b.quantity_reserved)
        for b in MedicationBatch.objects.filter(
            product=product, expiry_date__gte=timezone.localdate()
        )
    )

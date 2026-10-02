from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.pharmacy.constants import (
    ControlledSubstanceSchedule,
    QuarantineStatus,
    RecallStatus,
)
from apps.pharmacy.models import (
    ControlledSubstanceControl,
    InventoryQuarantine,
    ProductRecall,
    RecallBatch,
    StockMovement,
)
from apps.pharmacy.services.audit import record_audit
from apps.pharmacy.services.events import enqueue_event


def validate_controlled_dispensing(
    *, organization, product, quantity, second_checker_id=None, actor_id=None
):
    control = ControlledSubstanceControl.objects.filter(
        organization=organization, product=product, active=True
    ).first()
    if control is None or control.schedule == ControlledSubstanceSchedule.NONE:
        return None
    quantity = Decimal(str(quantity))
    if control.requires_double_check and second_checker_id is None:
        raise ValidationError(
            "Controlled-substance dispensing requires a second checker."
        )
    if (
        actor_id is not None
        and second_checker_id is not None
        and str(actor_id) == str(second_checker_id)
    ):
        raise ValidationError(
            "The pharmacist cannot also act as the controlled-substance second checker."
        )
    if control.max_daily_quantity is not None:
        today = timezone.localdate()
        consumed_today = sum(
            (
                movement.quantity
                for movement in StockMovement.objects.filter(
                    organization=organization,
                    batch__product=product,
                    movement_type="dispense",
                    created_at__date=today,
                )
            ),
            Decimal("0"),
        )
        if consumed_today + quantity > control.max_daily_quantity:
            raise ValidationError(
                "Requested quantity exceeds the controlled-substance daily limit."
            )
    return control


@transaction.atomic
def quarantine_batch(*, organization, batch, quantity, reason, actor_id=None):
    quantity = Decimal(str(quantity))
    if quantity <= 0:
        raise ValidationError("Quarantine quantity must be greater than zero.")
    locked = (
        batch.__class__.objects.select_for_update()
        .select_related("product")
        .get(pk=batch.pk)
    )
    if locked.product.organization_id != organization.id:
        raise ValidationError("Batch is outside the organization scope.")
    if quantity > locked.quantity_available:
        raise ValidationError("Cannot quarantine more stock than is available.")
    locked.quantity_available -= quantity
    locked.save(update_fields=["quantity_available", "updated_at"])
    record = InventoryQuarantine.objects.create(
        organization=organization,
        batch=locked,
        quantity=quantity,
        reason=reason,
        quarantined_by_id=getattr(actor_id, "pk", actor_id) if actor_id else None,
    )
    record_audit(
        organization=organization,
        action="inventory.quarantined",
        entity_type="MedicationBatch",
        entity_id=locked.id,
        actor_id=actor_id,
        payload={
            "quarantine_id": str(record.id),
            "quantity": str(quantity),
            "reason": reason,
        },
    )
    return record


@transaction.atomic
def release_quarantine(*, organization, quarantine, actor_id=None):
    locked = (
        InventoryQuarantine.objects.select_for_update()
        .select_related("batch__product")
        .get(pk=quarantine.pk)
    )
    if locked.organization_id != organization.id:
        raise ValidationError("Quarantine is outside the organization scope.")
    if locked.status != QuarantineStatus.QUARANTINED:
        return locked
    locked.batch.quantity_available += locked.quantity
    locked.batch.save(update_fields=["quantity_available", "updated_at"])
    locked.status = QuarantineStatus.RELEASED
    locked.released_by_id = getattr(actor_id, "pk", actor_id) if actor_id else None
    locked.released_at = timezone.now()
    locked.save(update_fields=["status", "released_by_id", "released_at", "updated_at"])
    record_audit(
        organization=organization,
        action="inventory.quarantine_released",
        entity_type="InventoryQuarantine",
        entity_id=locked.id,
        actor_id=actor_id,
        payload={"batch_id": str(locked.batch_id)},
    )
    return locked


@transaction.atomic
def initiate_recall(
    *, organization, product, recall_number, reason, batch_quantities, actor_id=None
):
    if product.organization_id != organization.id:
        raise ValidationError("Product is outside the organization scope.")
    recall = ProductRecall.objects.create(
        organization=organization,
        product=product,
        recall_number=recall_number,
        reason=reason,
        initiated_by_id=getattr(actor_id, "pk", actor_id) if actor_id else None,
        status=RecallStatus.IN_PROGRESS,
    )
    for item in batch_quantities:
        batch = item["batch"]
        quantity = Decimal(str(item["quantity"]))
        if batch.product_id != product.id or quantity <= 0:
            raise ValidationError("Recall batch quantity is invalid.")
        batch = batch.__class__.objects.select_for_update().get(pk=batch.pk)
        if quantity > batch.quantity_available:
            raise ValidationError("Recall quantity exceeds available stock.")
        batch.quantity_available -= quantity
        batch.save(update_fields=["quantity_available", "updated_at"])
        RecallBatch.objects.create(
            recall=recall, batch=batch, quantity_affected=quantity, quarantined=True
        )
    record_audit(
        organization=organization,
        action="product.recall_initiated",
        entity_type="ProductRecall",
        entity_id=recall.id,
        actor_id=actor_id,
        payload={"recall_number": recall_number, "product_id": str(product.id)},
    )
    enqueue_event(
        organization=organization,
        event_type="pharmacy.recall_initiated",
        aggregate_type="ProductRecall",
        aggregate_id=recall.id,
        payload={
            "recall_id": str(recall.id),
            "recall_number": recall_number,
            "product_id": str(product.id),
        },
    )
    return recall


__all__ = (
    "validate_controlled_dispensing",
    "quarantine_batch",
    "release_quarantine",
    "initiate_recall",
)

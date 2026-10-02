from django.db import transaction
from django.utils import timezone

from apps.imaging.constants.choices import ImagingOrderStatus
from apps.imaging.models import ImagingOrder
from apps.imaging.services.audit import record_event


@transaction.atomic
def create_imaging_order(
    *,
    tenant_id,
    patient_id,
    clinical_indication,
    order_number,
    ordering_provider_id=None,
    encounter_id=None,
    priority="routine",
    actor_id=None,
):
    order = ImagingOrder.objects.create(
        tenant_id=tenant_id,
        patient_id=patient_id,
        clinical_indication=clinical_indication,
        order_number=order_number,
        ordering_provider_id=ordering_provider_id,
        encounter_id=encounter_id,
        priority=priority,
        status=ImagingOrderStatus.ORDERED,
        ordered_at=timezone.now(),
    )
    record_event(
        tenant_id=tenant_id,
        event_type="order.created",
        entity_type="ImagingOrder",
        entity_id=order.id,
        actor_id=actor_id,
        payload={"order_number": order.order_number},
    )
    return order


@transaction.atomic
def cancel_order(*, order_id, tenant_id, reason, actor_id=None):
    order = ImagingOrder.objects.select_for_update().get(
        id=order_id, tenant_id=tenant_id
    )
    if order.status in {ImagingOrderStatus.COMPLETED, ImagingOrderStatus.CANCELLED}:
        raise ValueError("Order cannot be cancelled in its current state.")
    order.status = ImagingOrderStatus.CANCELLED
    order.cancelled_at = timezone.now()
    order.cancellation_reason = reason
    order.save(
        update_fields=["status", "cancelled_at", "cancellation_reason", "updated_at"]
    )
    record_event(
        tenant_id=tenant_id,
        event_type="order.cancelled",
        entity_type="ImagingOrder",
        entity_id=order.id,
        actor_id=actor_id,
        payload={"reason": reason},
    )
    return order


from .workflow import (
    cancel_order_workflow,
    complete_order,
    mark_order_ready,
    schedule_order,
    start_order,
)

__all__ = [
    "create_imaging_order",
    "cancel_order",
    "mark_order_ready",
    "schedule_order",
    "start_order",
    "complete_order",
    "cancel_order_workflow",
]

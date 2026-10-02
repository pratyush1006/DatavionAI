from django.db import transaction
from django.utils import timezone

from ..models import (
    Laboratory,
    LaboratoryAuditLog,
    LaboratoryOutboxEvent,
    LaboratorySlot,
    LaboratorySlotAllocation,
)
from .laboratory import LaboratoryServiceError


@transaction.atomic
def allocate_slot_for_appointment(
    *, organization_id, laboratory_id, slot_id, appointment_id, actor_id=None
):
    from apps.clinical.appointments.models import Appointment

    lab = Laboratory.objects.select_for_update().get(
        id=laboratory_id, organization_id=organization_id, is_deleted=False
    )
    slot = LaboratorySlot.objects.select_for_update().get(
        id=slot_id, laboratory_id=lab.id, is_deleted=False
    )
    appointment = Appointment.objects.select_for_update().get(
        id=appointment_id, organization_id=organization_id, is_deleted=False
    )
    if not lab.appointment_enabled:
        raise LaboratoryServiceError("Laboratory appointments are disabled.")
    if slot.ends_at <= timezone.now():
        raise LaboratoryServiceError("Appointment slot has expired.")
    if (
        appointment.scheduled_start != slot.starts_at
        or appointment.scheduled_end != slot.ends_at
    ):
        raise LaboratoryServiceError(
            "Appointment time does not match the laboratory slot."
        )
    if appointment.status in {"cancelled", "completed", "no_show"}:
        raise LaboratoryServiceError(
            "Appointment is not eligible for laboratory allocation."
        )
    allocation, created = LaboratorySlotAllocation.objects.get_or_create(
        slot=slot,
        appointment=appointment,
        defaults={"organization_id": organization_id, "status": "allocated"},
    )
    if created:
        if slot.booked_count >= slot.capacity:
            raise LaboratoryServiceError("Appointment slot is full.")
        slot.booked_count += 1
        slot.save(update_fields=["booked_count", "updated_at"])
        LaboratoryAuditLog.objects.create(
            organization_id=organization_id,
            actor_id=actor_id,
            action="appointment.allocated",
            entity_type="Appointment",
            entity_id=appointment.id,
            metadata={"laboratory_id": str(lab.id), "slot_id": str(slot.id)},
        )
        LaboratoryOutboxEvent.objects.create(
            organization_id=organization_id,
            event_type="laboratory.appointment.allocated",
            aggregate_type="Appointment",
            aggregate_id=appointment.id,
            payload={"laboratory_id": str(lab.id), "slot_id": str(slot.id)},
            available_at=timezone.now(),
        )
    return appointment


@transaction.atomic
def release_slot_for_appointment(
    *, organization_id, slot_id, appointment_id, actor_id=None
):
    from apps.clinical.appointments.models import Appointment

    appointment = Appointment.objects.select_for_update().get(
        id=appointment_id, organization_id=organization_id, is_deleted=False
    )
    slot = LaboratorySlot.objects.select_for_update().get(
        id=slot_id, laboratory__organization_id=organization_id, is_deleted=False
    )
    allocation = (
        LaboratorySlotAllocation.objects.select_for_update()
        .filter(
            slot=slot,
            appointment=appointment,
            organization_id=organization_id,
            status="allocated",
        )
        .first()
    )
    if allocation:
        allocation.status = "released"
        allocation.save(update_fields=["status", "updated_at"])
        if slot.booked_count > 0:
            slot.booked_count -= 1
            slot.save(update_fields=["booked_count", "updated_at"])
        LaboratoryAuditLog.objects.create(
            organization_id=organization_id,
            actor_id=actor_id,
            action="appointment.slot_released",
            entity_type="Appointment",
            entity_id=appointment.id,
            metadata={"slot_id": str(slot.id)},
        )
    return appointment

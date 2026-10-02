from django.db import transaction
from django.utils import timezone

from ..constants import OrderStatus, SpecimenStatus
from ..models import LaboratoryOrder, LaboratorySpecimen
from .audit import audit
from .events import event
from .laboratory import LaboratoryServiceError


@transaction.atomic
def receive_specimen(*, organization_id, specimen_id, actor_id=None):
    specimen = LaboratorySpecimen.objects.select_for_update().get(
        id=specimen_id, organization_id=organization_id, is_deleted=False
    )
    if specimen.status != SpecimenStatus.COLLECTED:
        raise LaboratoryServiceError("Only collected specimens can be received.")
    now = timezone.now()
    specimen.status = SpecimenStatus.RECEIVED
    specimen.received_at = now
    specimen.chain_of_custody = [
        *specimen.chain_of_custody,
        {
            "event": "received",
            "at": now.isoformat(),
            "actor_id": str(actor_id) if actor_id else None,
        },
    ]
    specimen.save(
        update_fields=["status", "received_at", "chain_of_custody", "updated_at"]
    )
    order = LaboratoryOrder.objects.select_for_update().get(
        id=specimen.order_id, organization_id=organization_id, is_deleted=False
    )
    order.status = OrderStatus.PROCESSING
    order.save(update_fields=["status", "updated_at"])
    audit(
        organization_id,
        actor_id,
        "specimen.received",
        "LaboratorySpecimen",
        specimen.id,
    )
    event(
        organization_id,
        "laboratory.specimen.received",
        "LaboratorySpecimen",
        specimen.id,
    )
    return specimen


@transaction.atomic
def start_processing(*, organization_id, specimen_id, actor_id=None):
    specimen = LaboratorySpecimen.objects.select_for_update().get(
        id=specimen_id, organization_id=organization_id, is_deleted=False
    )
    if specimen.status != SpecimenStatus.RECEIVED:
        raise LaboratoryServiceError("Only received specimens can enter processing.")
    specimen.status = SpecimenStatus.PROCESSING
    specimen.save(update_fields=["status", "updated_at"])
    audit(
        organization_id,
        actor_id,
        "specimen.processing_started",
        "LaboratorySpecimen",
        specimen.id,
    )
    event(
        organization_id,
        "laboratory.specimen.processing_started",
        "LaboratorySpecimen",
        specimen.id,
    )
    return specimen


@transaction.atomic
def complete_processing(*, organization_id, specimen_id, actor_id=None):
    specimen = LaboratorySpecimen.objects.select_for_update().get(
        id=specimen_id, organization_id=organization_id, is_deleted=False
    )
    if specimen.status != SpecimenStatus.PROCESSING:
        raise LaboratoryServiceError("Only processing specimens can be completed.")
    specimen.status = SpecimenStatus.COMPLETED
    specimen.save(update_fields=["status", "updated_at"])
    audit(
        organization_id,
        actor_id,
        "specimen.processing_completed",
        "LaboratorySpecimen",
        specimen.id,
    )
    event(
        organization_id,
        "laboratory.specimen.processing_completed",
        "LaboratorySpecimen",
        specimen.id,
    )
    return specimen


@transaction.atomic
def reject_specimen(*, organization_id, specimen_id, reason, actor_id=None):
    specimen = LaboratorySpecimen.objects.select_for_update().get(
        id=specimen_id, organization_id=organization_id, is_deleted=False
    )
    if specimen.status in {SpecimenStatus.COMPLETED, SpecimenStatus.REJECTED}:
        raise LaboratoryServiceError(
            "Specimen cannot be rejected in its current state."
        )
    if not reason or not reason.strip():
        raise LaboratoryServiceError("Specimen rejection requires a reason.")
    specimen.status = SpecimenStatus.REJECTED
    specimen.rejection_reason = reason.strip()
    specimen.save(update_fields=["status", "rejection_reason", "updated_at"])
    audit(
        organization_id,
        actor_id,
        "specimen.rejected",
        "LaboratorySpecimen",
        specimen.id,
        {"reason": reason.strip()},
    )
    event(
        organization_id,
        "laboratory.specimen.rejected",
        "LaboratorySpecimen",
        specimen.id,
    )
    return specimen

import uuid

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .constants import (
    AdmissionStatus,
    BedStatus,
    OPDVisitStatus,
    ReservationStatus,
)
from .models import (
    Admission,
    Bed,
    BedAssignment,
    BedReservation,
    OPDQueue,
    OPDVisit,
    OperationalEvent,
    PatientMovement,
)


def _assert_scope(*, obj, tenant, organization, label):
    if obj.tenant_id != tenant.id or obj.organization_id != organization.id:
        raise ValidationError(f"{label} is outside the active scope.")


def _assert_patient_scope(*, patient, tenant, organization):
    field_names = {field.name for field in patient._meta.get_fields()}
    if "tenant" in field_names and patient.tenant_id != tenant.id:
        raise ValidationError("Patient is outside the active tenant scope.")
    if "organization" in field_names and patient.organization_id != organization.id:
        raise ValidationError("Patient is outside the active organization scope.")


def _event(tenant, organization, event_type, entity, patient_id=None, metadata=None):
    return OperationalEvent.objects.create(
        tenant=tenant,
        organization=organization,
        event_type=event_type,
        entity_type=entity.__class__.__name__,
        entity_id=entity.uuid,
        patient_id=patient_id,
        correlation_id=uuid.uuid4().hex,
        metadata=metadata or {},
    )


@transaction.atomic
def reserve_bed(
    *,
    bed,
    patient,
    tenant,
    organization,
    reserved_from=None,
    reserved_until=None,
    reference="",
    notes="",
):
    _assert_patient_scope(patient=patient, tenant=tenant, organization=organization)
    bed = (
        Bed.objects.select_for_update()
        .select_related("room", "room__unit")
        .get(pk=bed.pk)
    )
    _assert_scope(obj=bed, tenant=tenant, organization=organization, label="Bed")
    if not bed.active or bed.status not in (
        BedStatus.AVAILABLE.value,
        BedStatus.RESERVED.value,
    ):
        raise ValidationError("Bed is not reservable.")
    if (
        BedReservation.objects.select_for_update()
        .filter(bed=bed, status=ReservationStatus.ACTIVE.value)
        .exists()
    ):
        raise ValidationError("Bed already has an active reservation.")
    reservation = BedReservation.objects.create(
        tenant=tenant,
        organization=organization,
        bed=bed,
        patient=patient,
        reserved_from=reserved_from or timezone.now(),
        reserved_until=reserved_until,
        reference=reference,
        notes=notes,
    )
    bed.status = BedStatus.RESERVED.value
    bed.save(update_fields=("status", "updated_at"))
    _event(
        tenant,
        organization,
        "bed_reserved",
        bed,
        patient.pk,
        {"reservation_id": str(reservation.uuid)},
    )
    return reservation


@transaction.atomic
def cancel_bed_reservation(*, reservation, tenant, organization):
    reservation = (
        BedReservation.objects.select_for_update()
        .select_related("bed")
        .get(pk=reservation.pk)
    )
    _assert_scope(
        obj=reservation, tenant=tenant, organization=organization, label="Reservation"
    )
    if reservation.status != ReservationStatus.ACTIVE.value:
        return reservation
    reservation.status = ReservationStatus.CANCELLED.value
    reservation.save(update_fields=("status", "updated_at"))
    bed = Bed.objects.select_for_update().get(pk=reservation.bed_id)
    if not BedReservation.objects.filter(
        bed=bed, status=ReservationStatus.ACTIVE.value
    ).exists():
        if not BedAssignment.objects.filter(bed=bed, active=True).exists():
            bed.status = BedStatus.AVAILABLE.value
            bed.save(update_fields=("status", "updated_at"))
    _event(
        tenant, organization, "bed_reservation_cancelled", bed, reservation.patient_id
    )
    return reservation


@transaction.atomic
def assign_bed(
    *, bed, patient, tenant, organization, admission_reference="", reservation=None
):
    _assert_patient_scope(patient=patient, tenant=tenant, organization=organization)
    bed = (
        Bed.objects.select_for_update()
        .select_related("room", "room__unit")
        .get(pk=bed.pk)
    )
    _assert_scope(obj=bed, tenant=tenant, organization=organization, label="Bed")
    if not bed.active or bed.status not in (
        BedStatus.AVAILABLE.value,
        BedStatus.RESERVED.value,
    ):
        raise ValidationError("Bed is not assignable.")
    if BedAssignment.objects.select_for_update().filter(bed=bed, active=True).exists():
        raise ValidationError("Bed already has an active assignment.")
    if reservation is not None:
        reservation = BedReservation.objects.select_for_update().get(pk=reservation.pk)
        _assert_scope(
            obj=reservation,
            tenant=tenant,
            organization=organization,
            label="Reservation",
        )
        if (
            reservation.bed_id != bed.pk
            or reservation.status != ReservationStatus.ACTIVE.value
        ):
            raise ValidationError("Reservation is not valid for this bed.")
        reservation.status = ReservationStatus.FULFILLED.value
        reservation.save(update_fields=("status", "updated_at"))
    assignment = BedAssignment.objects.create(
        tenant=tenant,
        organization=organization,
        bed=bed,
        patient=patient,
        admission_reference=admission_reference,
        started_at=timezone.now(),
    )
    bed.status = BedStatus.OCCUPIED.value
    bed.save(update_fields=("status", "updated_at"))
    _event(
        tenant,
        organization,
        "bed_assigned",
        bed,
        patient.pk,
        {"assignment_id": str(assignment.uuid)},
    )
    return assignment


@transaction.atomic
def release_bed(*, assignment, tenant, organization):
    assignment = (
        BedAssignment.objects.select_for_update()
        .select_related("bed", "patient")
        .get(pk=assignment.pk)
    )
    _assert_scope(
        obj=assignment, tenant=tenant, organization=organization, label="Assignment"
    )
    if not assignment.active:
        return assignment
    assignment.active = False
    assignment.ended_at = timezone.now()
    assignment.save(update_fields=("active", "ended_at", "updated_at"))
    bed = Bed.objects.select_for_update().get(pk=assignment.bed_id)
    bed.status = BedStatus.CLEANING.value
    bed.save(update_fields=("status", "updated_at"))
    _event(tenant, organization, "bed_released", bed, assignment.patient_id)
    return assignment


@transaction.atomic
def transfer_patient(
    *, admission, to_unit, to_bed, tenant, organization, reason="", icu=False
):
    admission = Admission.objects.select_for_update().get(pk=admission.pk)
    _assert_scope(
        obj=admission, tenant=tenant, organization=organization, label="Admission"
    )
    if admission.status != AdmissionStatus.ADMITTED.value:
        raise ValidationError("Only admitted patients can be transferred.")
    if not admission.bed_assignment_id:
        raise ValidationError("Admission has no active bed assignment.")
    to_unit = type(to_unit).objects.select_for_update().get(pk=to_unit.pk)
    _assert_scope(
        obj=to_unit, tenant=tenant, organization=organization, label="Destination unit"
    )
    to_bed = Bed.objects.select_for_update().get(pk=to_bed.pk)
    _assert_scope(
        obj=to_bed, tenant=tenant, organization=organization, label="Destination bed"
    )
    if to_bed.room.unit_id != to_unit.pk:
        raise ValidationError("Destination bed does not belong to destination unit.")
    old_assignment = (
        BedAssignment.objects.select_for_update()
        .select_related("bed")
        .get(pk=admission.bed_assignment_id)
    )
    old_bed = old_assignment.bed
    if old_bed.pk == to_bed.pk:
        raise ValidationError("Destination bed must differ from current bed.")
    old_unit = admission.unit
    new_assignment = assign_bed(
        bed=to_bed,
        patient=admission.patient,
        tenant=tenant,
        organization=organization,
        admission_reference=admission.admission_number,
    )
    release_bed(assignment=old_assignment, tenant=tenant, organization=organization)
    admission.unit = to_unit
    admission.bed_assignment = new_assignment
    admission.save(update_fields=("unit", "bed_assignment", "updated_at"))
    movement = PatientMovement.objects.create(
        tenant=tenant,
        organization=organization,
        patient=admission.patient,
        admission=admission,
        from_unit=old_unit,
        to_unit=to_unit,
        from_bed=old_bed,
        to_bed=to_bed,
        movement_type="icu_transfer" if icu else "transfer",
        occurred_at=timezone.now(),
        reason=reason,
    )
    _event(
        tenant,
        organization,
        "transferred",
        movement,
        admission.patient.pk,
        {"icu": icu},
    )
    return movement


@transaction.atomic
def discharge_patient(*, admission, tenant, organization):
    admission = Admission.objects.select_for_update().get(pk=admission.pk)
    _assert_scope(
        obj=admission, tenant=tenant, organization=organization, label="Admission"
    )
    if admission.status != AdmissionStatus.ADMITTED.value:
        raise ValidationError("Only admitted patients can be discharged.")
    if admission.bed_assignment_id:
        release_bed(
            assignment=admission.bed_assignment,
            tenant=tenant,
            organization=organization,
        )
    admission.status = AdmissionStatus.DISCHARGED.value
    admission.discharged_at = timezone.now()
    admission.save(update_fields=("status", "discharged_at", "updated_at"))
    _event(tenant, organization, "discharged", admission, admission.patient.pk)
    return admission


@transaction.atomic
def register_opd_visit(*, queue, patient, tenant, organization, encounter_reference=""):
    _assert_patient_scope(patient=patient, tenant=tenant, organization=organization)
    queue = OPDQueue.objects.select_for_update().get(pk=queue.pk)
    _assert_scope(
        obj=queue, tenant=tenant, organization=organization, label="OPD queue"
    )
    if queue.status != "open":
        raise ValidationError("OPD queue is not open.")
    queue.current_token += 1
    queue.save(update_fields=("current_token", "updated_at"))
    visit = OPDVisit.objects.create(
        tenant=tenant,
        organization=organization,
        patient=patient,
        queue=queue,
        token_number=queue.current_token,
        status=OPDVisitStatus.WAITING.value,
        registered_at=timezone.now(),
        encounter_reference=encounter_reference,
    )
    _event(
        tenant,
        organization,
        "opd_registered",
        visit,
        patient.pk,
        {"token": visit.token_number},
    )
    return visit


@transaction.atomic
def complete_room_cleaning(*, bed, tenant, organization):
    bed = Bed.objects.select_for_update().get(pk=bed.pk)
    _assert_scope(obj=bed, tenant=tenant, organization=organization, label="Bed")
    if bed.status != BedStatus.CLEANING.value:
        raise ValidationError("Bed is not awaiting cleaning completion.")
    bed.status = BedStatus.AVAILABLE.value
    bed.save(update_fields=("status", "updated_at"))
    _event(tenant, organization, "bed_cleaning_completed", bed)
    return bed

import uuid

from django.db import models

from .constants import (
    AdmissionStatus,
    BedStatus,
    FacilityStatus,
    MovementType,
    OPDVisitStatus,
    RoomStatus,
)


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Facility(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="hospital_facilities",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="hospital_facilities",
    )
    name = models.CharField(max_length=180)
    code = models.CharField(max_length=60)
    status = models.CharField(
        max_length=30,
        choices=[(x.value, x.value) for x in FacilityStatus],
        default=FacilityStatus.ACTIVE,
    )
    address = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "hospital_operations_facilities"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"),
                name="hop_fac_org_code_uniq",
            )
        ]


class OperationalUnit(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="hospital_units",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="hospital_units",
    )
    facility = models.ForeignKey(
        Facility, on_delete=models.PROTECT, related_name="units"
    )
    name = models.CharField(max_length=180)
    code = models.CharField(max_length=60)
    unit_type = models.CharField(max_length=50, default="ward")
    specialty = models.CharField(max_length=120, blank=True)
    active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "hospital_operations_units"
        constraints = [
            models.UniqueConstraint(
                fields=("facility", "code"),
                name="hop_unit_fac_code_uniq",
            )
        ]


class Room(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="hospital_rooms",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="hospital_rooms",
    )
    facility = models.ForeignKey(
        Facility, on_delete=models.PROTECT, related_name="rooms"
    )
    unit = models.ForeignKey(
        OperationalUnit, on_delete=models.PROTECT, related_name="rooms"
    )
    number = models.CharField(max_length=60)
    room_type = models.CharField(max_length=60, default="standard")
    floor = models.CharField(max_length=60, blank=True)
    status = models.CharField(
        max_length=40,
        choices=[(x.value, x.value) for x in RoomStatus],
        default=RoomStatus.AVAILABLE,
    )
    capacity = models.PositiveIntegerField(default=1)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "hospital_operations_rooms"
        constraints = [
            models.UniqueConstraint(
                fields=("unit", "number"),
                name="hop_room_unit_number_uniq",
            ),
            models.CheckConstraint(
                condition=models.Q(capacity__gte=1),
                name="hop_room_capacity_positive",
            ),
        ]


class Bed(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="hospital_beds",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="hospital_beds",
    )
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="beds")
    label = models.CharField(max_length=80)
    bed_type = models.CharField(max_length=60, default="standard")
    status = models.CharField(
        max_length=40,
        choices=[(x.value, x.value) for x in BedStatus],
        default=BedStatus.AVAILABLE,
    )
    isolation_capable = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "hospital_operations_beds"
        constraints = [
            models.UniqueConstraint(
                fields=("room", "label"),
                name="hop_bed_room_label_uniq",
            )
        ]


class BedAssignment(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="hospital_bed_assignments",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="hospital_bed_assignments",
    )
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name="assignments")
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="hospital_bed_assignments",
    )
    admission_reference = models.CharField(max_length=120, blank=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "hospital_operations_bed_assignments"
        constraints = [
            models.UniqueConstraint(
                fields=("bed",),
                condition=models.Q(active=True),
                name="hop_one_active_bed_assignment",
            )
        ]


class BedReservation(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="hospital_bed_reservations",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="hospital_bed_reservations",
    )
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name="reservations")
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="hospital_bed_reservations",
    )
    reserved_from = models.DateTimeField()
    reserved_until = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="active")
    reference = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "hospital_operations_bed_reservations"
        constraints = [
            models.UniqueConstraint(
                fields=("bed",),
                condition=models.Q(status="active"),
                name="hop_one_active_bed_reservation",
            ),
            models.CheckConstraint(
                condition=models.Q(reserved_until__isnull=True)
                | models.Q(reserved_until__gt=models.F("reserved_from")),
                name="hop_reservation_time_valid",
            ),
        ]


class Admission(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="hospital_admissions",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="hospital_admissions",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="hospital_admissions",
    )
    unit = models.ForeignKey(
        OperationalUnit, on_delete=models.PROTECT, related_name="admissions"
    )
    bed_assignment = models.OneToOneField(
        BedAssignment,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="admission",
    )
    admission_number = models.CharField(max_length=80)
    admitted_at = models.DateTimeField()
    discharged_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=30,
        choices=[(x.value, x.value) for x in AdmissionStatus],
        default=AdmissionStatus.ADMITTED.value,
    )
    reason = models.TextField(blank=True)

    class Meta:
        db_table = "hospital_operations_admissions"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "admission_number"),
                name="hop_adm_org_number_uniq",
            ),
        ]


class PatientMovement(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="hospital_movements",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="hospital_movements",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="hospital_movements",
    )
    admission = models.ForeignKey(
        Admission, on_delete=models.PROTECT, related_name="movements"
    )
    from_unit = models.ForeignKey(
        OperationalUnit,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="outgoing_movements",
    )
    to_unit = models.ForeignKey(
        OperationalUnit,
        on_delete=models.PROTECT,
        related_name="incoming_movements",
    )
    from_bed = models.ForeignKey(
        Bed,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="outgoing_movements",
    )
    to_bed = models.ForeignKey(
        Bed,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="incoming_movements",
    )
    movement_type = models.CharField(
        max_length=40,
        choices=[(x.value, x.value) for x in MovementType],
    )
    occurred_at = models.DateTimeField()
    reason = models.TextField(blank=True)

    class Meta:
        db_table = "hospital_operations_patient_movements"


class OPDQueue(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="opd_queues",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="opd_queues",
    )
    unit = models.ForeignKey(
        OperationalUnit, on_delete=models.PROTECT, related_name="opd_queues"
    )
    name = models.CharField(max_length=160)
    queue_date = models.DateField()
    current_token = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="open")

    class Meta:
        db_table = "hospital_operations_opd_queues"
        constraints = [
            models.UniqueConstraint(
                fields=("unit", "queue_date"),
                name="hop_opd_unit_date_uniq",
            )
        ]


class OPDVisit(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="opd_visits",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="opd_visits",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="opd_visits",
    )
    queue = models.ForeignKey(OPDQueue, on_delete=models.PROTECT, related_name="visits")
    token_number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=30,
        choices=[(x.value, x.value) for x in OPDVisitStatus],
        default=OPDVisitStatus.REGISTERED,
    )
    registered_at = models.DateTimeField()
    called_at = models.DateTimeField(null=True, blank=True)
    consultation_started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    encounter_reference = models.CharField(max_length=160, blank=True)

    class Meta:
        db_table = "hospital_operations_opd_visits"
        constraints = [
            models.UniqueConstraint(
                fields=("queue", "token_number"),
                name="hop_opd_queue_token_uniq",
            )
        ]


class OperationalEvent(Timestamped):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="hospital_operational_events",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="hospital_operational_events",
    )
    event_type = models.CharField(max_length=80)
    entity_type = models.CharField(max_length=80)
    entity_id = models.UUIDField()
    patient_id = models.UUIDField(null=True, blank=True)
    correlation_id = models.CharField(max_length=80, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "hospital_operations_events"

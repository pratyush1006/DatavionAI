from django.db import models

from apps.clinical.appointments.models import Appointment
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization

from .laboratory import Laboratory


class LaboratorySlot(BaseModel):
    objects = BaseManager()
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE, related_name="appointment_slots"
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=1)
    booked_count = models.PositiveIntegerField(default=0)
    collection_type = models.CharField(max_length=20, default="laboratory")
    status = models.CharField(max_length=20, default="available")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("laboratory", "starts_at", "collection_type"),
                name="uq_lab_slot_start_type",
            ),
            models.CheckConstraint(
                condition=models.Q(ends_at__gt=models.F("starts_at")),
                name="ck_lab_slot_time",
            ),
            models.CheckConstraint(
                condition=models.Q(booked_count__lte=models.F("capacity")),
                name="ck_lab_slot_capacity",
            ),
        ]


class LaboratorySlotAllocation(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="laboratory_slot_allocations",
    )
    slot = models.ForeignKey(
        LaboratorySlot, on_delete=models.PROTECT, related_name="allocations"
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.PROTECT,
        related_name="laboratory_slot_allocations",
    )
    status = models.CharField(max_length=20, default="allocated")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("slot", "appointment"), name="uq_lab_slot_appointment"
            )
        ]

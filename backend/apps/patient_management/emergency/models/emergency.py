"""Emergency contact model for the Patient Management domain."""

from __future__ import annotations

import uuid

from django.db import models

from apps.patient_management.emergency.constants import (
    EmergencyContactPriority,
    EmergencyContactType,
    EmergencyRecordStatus,
)
from apps.patient_management.emergency.managers import (
    EmergencyRecordManager,
)
from apps.patient_management.emergency.validators import (
    validate_contact_name,
    validate_contact_phone,
)
from apps.patient_management.patients.models import Patient


class EmergencyContact(models.Model):
    """Store an emergency contact associated with a canonical Patient."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="patient_emergency_contacts",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
    )
    name = models.CharField(
        max_length=255,
        validators=[validate_contact_name],
    )
    relationship = models.CharField(
        max_length=32,
        choices=EmergencyContactType.choices,
    )
    phone = models.CharField(
        max_length=64,
        validators=[validate_contact_phone],
    )
    alternate_phone = models.CharField(
        max_length=64,
        blank=True,
    )
    email = models.EmailField(
        blank=True,
    )
    priority = models.CharField(
        max_length=16,
        choices=EmergencyContactPriority.choices,
        default=EmergencyContactPriority.SECONDARY,
    )
    status = models.CharField(
        max_length=16,
        choices=EmergencyRecordStatus.choices,
        default=EmergencyRecordStatus.ACTIVE,
    )
    notes = models.TextField(
        blank=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = EmergencyRecordManager()

    class Meta:
        """Define database constraints and indexes."""

        db_table = "patient_emergency_contacts"
        ordering = ("-priority", "name")
        indexes = (
            models.Index(fields=("organization", "patient")),
            models.Index(fields=("organization", "status")),
            models.Index(fields=("patient", "is_deleted")),
        )

    def __str__(self) -> str:
        """Return a human-readable emergency contact label."""

        return f"{self.name} - {self.patient_id}"

    def normalize(self) -> None:
        """Normalize user-entered emergency contact fields."""

        self.name = " ".join(self.name.strip().split())
        self.phone = " ".join(self.phone.strip().split())
        self.alternate_phone = " ".join(
            self.alternate_phone.strip().split(),
        )
        self.email = self.email.strip().lower()
        self.notes = self.notes.strip()


__all__ = ("EmergencyContact",)

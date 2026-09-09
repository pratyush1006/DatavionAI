"""Patient Communication persistence model."""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.communication.constants import (
    CommunicationChannel,
    CommunicationDirection,
    CommunicationStatus,
    CommunicationType,
)
from apps.patient_management.communication.managers import CommunicationManager
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class PatientCommunication(BaseModel):
    """Record a tenant-scoped communication interaction with a patient."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_communications",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="communications",
    )
    channel = models.CharField(max_length=20, choices=CommunicationChannel.choices)
    direction = models.CharField(max_length=20, choices=CommunicationDirection.choices)
    communication_type = models.CharField(
        max_length=30,
        choices=CommunicationType.choices,
        default=CommunicationType.GENERAL,
    )
    status = models.CharField(
        max_length=20,
        choices=CommunicationStatus.choices,
        default=CommunicationStatus.DRAFT,
        db_index=True,
    )
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    external_reference = models.CharField(max_length=255, blank=True)
    occurred_at = models.DateTimeField(null=True, blank=True, db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    failed_reason = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_patient_communications",
    )

    objects = CommunicationManager()

    class Meta:
        """Database metadata for Patient Communication."""

        db_table = "patient_communications"
        ordering = ("-occurred_at", "-created_at")
        indexes = [
            models.Index(fields=("organization", "patient", "occurred_at")),
            models.Index(fields=("organization", "status", "is_deleted")),
            models.Index(fields=("organization", "channel", "occurred_at")),
        ]

    def __str__(self) -> str:
        """Return a readable communication identifier."""
        return f"{self.patient_id} - {self.channel} - {self.status}"


__all__ = ("PatientCommunication",)

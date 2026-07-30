"""
Communication models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.patient_management.communication.constants import (
    CommunicationChannel,
    CommunicationDirection,
    CommunicationStatus,
)
from apps.platform.organizations.models import Organization


class PatientCommunication(BaseModel):
    """
    A communication record sent to or received from a patient.
    """

    objects = BaseManager()

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

    channel = models.CharField(
        max_length=20,
        choices=CommunicationChannel.choices,
        default=CommunicationChannel.EMAIL,
    )

    direction = models.CharField(
        max_length=20,
        choices=CommunicationDirection.choices,
        default=CommunicationDirection.OUTBOUND,
    )

    status = models.CharField(
        max_length=20,
        choices=CommunicationStatus.choices,
        default=CommunicationStatus.PENDING,
        db_index=True,
    )

    subject = models.CharField(
        max_length=255,
        blank=True,
    )

    message = models.TextField(
        help_text="Communication body.",
    )

    recipient = models.CharField(
        max_length=255,
        blank=True,
        help_text="Recipient address / number.",
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    template = models.CharField(
        max_length=100,
        blank=True,
        help_text="Communication template identifier, if used.",
    )

    reference_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="External provider reference id.",
    )

    class Meta:
        db_table = "patient_communications"

        verbose_name = "Patient Communication"

        verbose_name_plural = "Patient Communications"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "status",
                ],
                name="comm_org_pat_status_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.get_channel_display()} - {self.get_status_display()}"


__all__ = [
    "PatientCommunication",
]

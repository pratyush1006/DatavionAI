"""
Prior authorization model.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.constants import (
    DEFAULT_AUTHORIZATION_STATUS,
    AuthorizationServiceType,
    AuthorizationStatus,
)
from apps.insurance.models.enrollment import Enrollment
from apps.platform.organizations.models import Organization


class Authorization(BaseModel):
    """
    Represents a prior authorization request for a service.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="authorizations",
        help_text="Organization that owns the authorization.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="authorizations",
        help_text="Patient requiring the authorized service.",
    )

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="authorizations",
        help_text="Enrollment used for the authorization.",
    )

    authorization_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique authorization number.",
    )

    service_type = models.CharField(
        max_length=20,
        choices=AuthorizationServiceType.choices,
        help_text="Type of service being authorized.",
    )

    requested_service = models.TextField(
        help_text="Description of the requested service.",
    )

    requested_date = models.DateField(
        help_text="Date the service was requested.",
    )

    authorized_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the service was authorized.",
    )

    expiration_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the authorization expires.",
    )

    status = models.CharField(
        max_length=20,
        choices=AuthorizationStatus.choices,
        default=DEFAULT_AUTHORIZATION_STATUS,
        help_text="Authorization lifecycle status.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the authorization.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the authorization was created.",
    )

    class Meta:
        db_table = "insurance_authorizations"

        verbose_name = "Prior Authorization"

        verbose_name_plural = "Prior Authorizations"

        ordering = (
            "patient",
            "requested_date",
        )

        indexes = [
            models.Index(
                fields=[
                    "patient",
                    "status",
                ],
                name="auth_patient_status_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="authorization_org_status_idx",
            ),
            models.Index(
                fields=[
                    "enrollment",
                    "status",
                ],
                name="auth_enroll_status_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Return the authorization display name.
        """

        return f"{self.authorization_number} ({self.status})"


__all__ = [
    "Authorization",
]

"""
Patient model.
"""

from __future__ import annotations

from django.db import models

from apps.common.validators import phone_validator
from apps.core.models import BaseManager, BaseModel
from apps.organizations.models import Organization
from apps.patients.constants import (
    DEFAULT_PATIENT_STATUS,
    BloodGroup,
    PatientGender,
    PatientMaritalStatus,
    PatientStatus,
)


class Patient(BaseModel):
    """
    Represents a patient within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patients",
        help_text="Organization that owns the patient record.",
    )

    mrn = models.CharField(
        max_length=30,
        help_text="Medical Record Number (MRN).",
    )

    first_name = models.CharField(
        max_length=100,
        help_text="Patient first name.",
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Patient middle name.",
    )

    last_name = models.CharField(
        max_length=100,
        help_text="Patient last name.",
    )

    preferred_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Preferred display name.",
    )

    date_of_birth = models.DateField(
        help_text="Patient date of birth.",
    )

    gender = models.CharField(
        max_length=20,
        choices=PatientGender.choices,
        help_text="Patient gender.",
    )

    marital_status = models.CharField(
        max_length=20,
        choices=PatientMaritalStatus.choices,
        blank=True,
        help_text="Patient marital status.",
    )

    blood_group = models.CharField(
        max_length=20,
        choices=BloodGroup.choices,
        blank=True,
        help_text="Patient blood group.",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        help_text="Primary contact phone number.",
    )

    email = models.EmailField(
        blank=True,
        help_text="Primary contact email.",
    )

    address = models.TextField(
        blank=True,
        help_text="Patient address.",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        help_text="City.",
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        help_text="State.",
    )

    country = models.CharField(
        max_length=100,
        default="India",
        help_text="Country.",
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="Postal code.",
    )

    status = models.CharField(
        max_length=20,
        choices=PatientStatus.choices,
        default=DEFAULT_PATIENT_STATUS,
        db_index=True,
        help_text="Patient lifecycle status.",
    )

    class Meta:
        db_table = "patients"

        verbose_name = "Patient"

        verbose_name_plural = "Patients"

        ordering = (
            "first_name",
            "last_name",
        )

        indexes = [
            models.Index(
                fields=[
                    "last_name",
                    "first_name",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "is_active",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "mrn",
                ],
                name="unique_patient_mrn_per_organization",
            ),
        ]

    @property
    def full_name(
        self,
    ) -> str:
        """
        Return the patient's complete name.
        """

        return " ".join(
            part
            for part in (
                self.first_name,
                self.middle_name,
                self.last_name,
            )
            if part
        )

    def __str__(
        self,
    ) -> str:
        """
        Return the patient display name.
        """

        return f"{self.full_name} ({self.mrn})"


__all__ = [
    "Patient",
]

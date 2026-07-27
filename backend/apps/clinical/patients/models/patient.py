"""
Patient model.
"""

from __future__ import annotations

from datetime import date

from django.db import models

from apps.clinical.patients.constants import (
    DEFAULT_PATIENT_STATUS,
    BloodGroup,
    PatientGender,
    PatientMaritalStatus,
    PatientStatus,
)
from apps.common.validators import phone_validator
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


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
            "last_name",
            "first_name",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="patient_org_status_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "last_name",
                    "first_name",
                ],
                name="patient_org_name_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "is_active",
                ],
                name="patient_org_active_idx",
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
        Return the patient's legal full name.
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

    @property
    def display_name(
        self,
    ) -> str:
        """
        Return the preferred display name if available,
        otherwise return the patient's legal full name.
        """

        return self.preferred_name or self.full_name

    @property
    def age(
        self,
    ) -> int:
        """
        Return the patient's age in completed years.
        """

        today = date.today()

        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (
                    self.date_of_birth.month,
                    self.date_of_birth.day,
                )
            )
        )

    def __str__(
        self,
    ) -> str:
        """
        Return the patient display name.
        """

        return f"{self.display_name} ({self.mrn})"


__all__ = [
    "Patient",
]

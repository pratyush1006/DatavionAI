"""
Patient Profile models.

Stores extended demographic, linguistic, cultural, and socio-economic
information for a patient. Contact details, addresses, identifiers,
preferences, and clinical information are maintained in their respective
bounded contexts.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.patient_management.patients.models import Patient
from apps.patient_management.profile.constants import (
    EducationLevel,
    EmploymentStatus,
    LanguageProficiency,
)
from apps.platform.organizations.models import Organization


class PatientProfile(BaseModel):
    """
    Extended demographic profile for a patient.

    A patient can have at most one profile within the owning organization.
    The profile intentionally excludes contact information, identifiers,
    addresses, consent, documents, preferences, and clinical data.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_profiles",
        help_text="Organization that owns the patient profile.",
    )

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="Patient associated with this profile.",
    )

    preferred_language = models.CharField(
        max_length=50,
        default="English",
        help_text="Patient's preferred language.",
    )

    language_proficiency = models.CharField(
        max_length=20,
        choices=LanguageProficiency.choices,
        default=LanguageProficiency.FLUENT,
        help_text="Patient's proficiency in the preferred language.",
    )

    nationality = models.CharField(
        max_length=100,
        blank=True,
        help_text="Patient nationality.",
    )

    religion = models.CharField(
        max_length=100,
        blank=True,
        help_text="Religion (optional).",
    )

    ethnicity = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ethnicity (optional).",
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
        help_text="Patient occupation.",
    )

    employment_status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        blank=True,
        help_text="Employment status.",
    )

    education_level = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
        blank=True,
        help_text="Highest education level.",
    )

    income_bracket = models.CharField(
        max_length=50,
        blank=True,
        help_text="Income bracket.",
    )

    interpreter_required = models.BooleanField(
        default=False,
        help_text="Whether interpreter assistance is required.",
    )

    class Meta:
        db_table = "patient_profiles"
        verbose_name = "Patient Profile"
        verbose_name_plural = "Patient Profiles"
        ordering = ("patient_id",)

        indexes = [
            models.Index(
                fields=("organization", "patient"),
                name="profile_org_patient_idx",
            ),
        ]

    def clean(self) -> None:
        """
        Validate and normalize profile data.

        The patient and profile must belong to the same organization.
        """

        super().clean()

        if self.patient_id and self.organization_id:
            patient_organization_id = (
                Patient.objects.filter(
                    pk=self.patient_id,
                )
                .values_list(
                    "organization_id",
                    flat=True,
                )
                .first()
            )

            if (
                patient_organization_id is not None
                and patient_organization_id != self.organization_id
            ):
                raise ValidationError(
                    {
                        "patient": (
                            "The patient must belong to the profile organization."
                        ),
                    }
                )

        self.preferred_language = self.preferred_language.strip()
        self.nationality = self.nationality.strip()
        self.religion = self.religion.strip()
        self.ethnicity = self.ethnicity.strip()
        self.occupation = self.occupation.strip()
        self.income_bracket = self.income_bracket.strip()

    @property
    def requires_interpreter(self) -> bool:
        """
        Return whether interpreter assistance is required.
        """

        return self.interpreter_required

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return f"Profile - {self.patient}"


__all__ = [
    "PatientProfile",
]

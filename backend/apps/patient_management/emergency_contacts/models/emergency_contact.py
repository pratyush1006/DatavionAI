"""
Emergency contact model.
"""

from __future__ import annotations

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization

from ..constants import (
    EmergencyContactAvailability,
    EmergencyContactRelationship,
    EmergencyContactStatus,
    PreferredContactMethod,
)
from ..validators import (
    validate_email_address,
    validate_emergency_contact_number,
    validate_notes,
    validate_phone_number,
)


class EmergencyContact(
    BaseModel,
):
    """
    Patient emergency contact.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
    )

    emergency_contact_number = models.CharField(
        max_length=30,
        validators=[
            validate_emergency_contact_number,
        ],
    )

    first_name = models.CharField(
        max_length=100,
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
    )

    relationship = models.CharField(
        max_length=50,
        choices=EmergencyContactRelationship.choices,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    mobile_number = models.CharField(
        max_length=20,
        validators=[
            validate_phone_number,
        ],
    )

    alternate_mobile_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            validate_phone_number,
        ],
    )

    home_phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            validate_phone_number,
        ],
    )

    work_phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            validate_phone_number,
        ],
    )

    email = models.EmailField(
        blank=True,
        validators=[
            validate_email_address,
        ],
    )

    preferred_contact_method = models.CharField(
        max_length=20,
        choices=PreferredContactMethod.choices,
        default=PreferredContactMethod.MOBILE,
    )

    address_line_1 = models.CharField(
        max_length=255,
        blank=True,
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    priority_order = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )

    availability = models.CharField(
        max_length=30,
        choices=EmergencyContactAvailability.choices,
        default=EmergencyContactAvailability.ALWAYS,
    )

    status = models.CharField(
        max_length=20,
        choices=EmergencyContactStatus.choices,
        default=EmergencyContactStatus.ACTIVE,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    is_legal_guardian = models.BooleanField(
        default=False,
    )

    has_medical_power_of_attorney = models.BooleanField(
        default=False,
    )

    notes = models.TextField(
        blank=True,
        validators=[
            validate_notes,
        ],
    )

    class Meta:
        ordering = (
            "priority_order",
            "first_name",
            "last_name",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "emergency_contact_number",
                ],
                name="uniq_org_emergency_contact_number",
            ),
            models.UniqueConstraint(
                fields=[
                    "patient",
                    "priority_order",
                ],
                name="uniq_patient_priority_order",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "relationship",
                ],
            ),
            models.Index(
                fields=[
                    "is_primary",
                ],
            ),
            models.Index(
                fields=[
                    "is_verified",
                ],
            ),
        ]

    @property
    def full_name(
        self,
    ) -> str:
        """
        Return the full name.
        """

        return " ".join(
            part
            for part in [
                self.first_name,
                self.middle_name,
                self.last_name,
            ]
            if part
        )

    def __str__(
        self,
    ) -> str:
        return f"{self.emergency_contact_number} - {self.full_name}"

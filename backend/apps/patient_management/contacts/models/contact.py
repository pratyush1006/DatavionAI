"""
Patient contact model.
"""

from __future__ import annotations

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import AuditableModel
from apps.patient_management.contacts.constants import (
    ContactPurpose,
    ContactSource,
    ContactStatus,
    ContactType,
)
from apps.patient_management.contacts.validators import (
    validate_email_address,
    validate_phone_number,
)
from apps.patient_management.models import Patient
from apps.platform.organizations.models import Organization


class Contact(AuditableModel):
    """
    Stores patient contact information.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_contacts",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="contacts",
    )

    contact_type = models.CharField(
        max_length=20,
        choices=ContactType.choices,
    )

    purpose = models.CharField(
        max_length=20,
        choices=ContactPurpose.choices,
        default=ContactPurpose.PRIMARY,
    )

    value = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=20,
        choices=ContactStatus.choices,
        default=ContactStatus.UNVERIFIED,
    )

    source = models.CharField(
        max_length=20,
        choices=ContactSource.choices,
        default=ContactSource.PATIENT,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    is_preferred = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = _("Patient Contact")
        verbose_name_plural = _("Patient Contacts")
        ordering = (
            "patient",
            "-is_primary",
            "contact_type",
        )
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "contact_type",
                    "value",
                ],
                name="uniq_patient_contact",
            ),
            models.UniqueConstraint(
                fields=[
                    "patient",
                    "contact_type",
                ],
                condition=Q(
                    is_primary=True,
                ),
                name="uniq_primary_patient_contact",
            ),
        ]

    def clean(self) -> None:
        super().clean()

        self.value = self.value.strip()

        if self.contact_type == ContactType.EMAIL:
            validate_email_address(self.value)
        else:
            validate_phone_number(self.value)

    def __str__(self) -> str:
        return self.value


__all__ = [
    "Contact",
]

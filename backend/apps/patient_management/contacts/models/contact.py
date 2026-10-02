"""
Patient Contact model.

Represents organization-scoped contact information belonging to the
canonical Patient Management Patient aggregate.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
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
from apps.patient_management.contacts.managers import ContactManager
from apps.patient_management.contacts.validators import (
    validate_contact_value,
    validate_email_address,
    validate_phone_number,
)
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class Contact(AuditableModel):
    """
    Stores patient contact information.

    A Contact is always owned by an organization and associated with
    the canonical Patient Management Patient model.

    Mutation operations are expected to flow through the Contact
    service/workflow layer rather than being performed directly by
    API serializers or views.
    """

    objects = ContactManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_contacts",
        verbose_name=_("Organization"),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="contacts",
        verbose_name=_("Patient"),
    )

    contact_type = models.CharField(
        max_length=20,
        choices=ContactType.choices,
        verbose_name=_("Contact Type"),
    )

    purpose = models.CharField(
        max_length=20,
        choices=ContactPurpose.choices,
        default=ContactPurpose.PRIMARY,
        verbose_name=_("Purpose"),
    )

    value = models.CharField(
        max_length=255,
        verbose_name=_("Value"),
    )

    status = models.CharField(
        max_length=20,
        choices=ContactStatus.choices,
        default=ContactStatus.UNVERIFIED,
        verbose_name=_("Status"),
    )

    source = models.CharField(
        max_length=20,
        choices=ContactSource.choices,
        default=ContactSource.PATIENT,
        verbose_name=_("Source"),
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Primary"),
    )

    is_preferred = models.BooleanField(
        default=False,
        verbose_name=_("Preferred"),
    )

    class Meta:
        verbose_name = _("Patient Contact")
        verbose_name_plural = _("Patient Contacts")

        ordering = (
            "patient",
            "-is_primary",
            "-is_preferred",
            "contact_type",
            "created_at",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "contact_type",
                    "value",
                ),
                condition=Q(
                    is_deleted=False,
                ),
                name="uniq_patient_contact",
            ),
            models.UniqueConstraint(
                fields=(
                    "patient",
                    "contact_type",
                ),
                condition=Q(
                    is_primary=True,
                    is_deleted=False,
                ),
                name="uniq_primary_patient_contact",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "organization",
                    "patient",
                ),
                name="idx_contact_org_patient",
            ),
            models.Index(
                fields=(
                    "patient",
                    "contact_type",
                ),
                name="idx_contact_patient_type",
            ),
            models.Index(
                fields=(
                    "organization",
                    "status",
                ),
                name="idx_contact_org_status",
            ),
            models.Index(
                fields=(
                    "organization",
                    "contact_type",
                ),
                name="idx_contact_org_type",
            ),
            models.Index(
                fields=(
                    "organization",
                    "is_deleted",
                ),
                name="idx_contact_org_deleted",
            ),
        ]

    def clean(self) -> None:
        """
        Validate and normalize contact data.

        Validation is type-aware:

        - EMAIL → email validation
        - MOBILE/HOME/WORK/EMERGENCY/FAX → phone validation
        - OTHER → generic non-empty value validation
        """
        super().clean()

        self.value = (self.value or "").strip()

        if not self.value:
            raise ValidationError(
                {
                    "value": _(
                        "Contact value cannot be empty.",
                    ),
                },
            )

        if self.contact_type == ContactType.EMAIL:
            self.value = self.value.lower()

            validate_email_address(
                self.value,
            )

        elif self.contact_type in {
            ContactType.MOBILE,
            ContactType.HOME,
            ContactType.WORK,
            ContactType.EMERGENCY,
            ContactType.FAX,
        }:
            validate_phone_number(
                self.value,
            )

        elif self.contact_type == ContactType.OTHER:
            validate_contact_value(
                self.value,
            )

        else:
            raise ValidationError(
                {
                    "contact_type": _(
                        "Unsupported contact type.",
                    ),
                },
            )

        patient_organization_id = getattr(
            self.patient,
            "organization_id",
            None,
        )

        if (
            patient_organization_id is not None
            and patient_organization_id != self.organization_id
        ):
            raise ValidationError(
                {
                    "organization": _(
                        "The contact organization must match the patient organization.",
                    ),
                },
            )

        if self.is_primary and self.status == ContactStatus.INACTIVE:
            raise ValidationError(
                {
                    "is_primary": _(
                        "An inactive contact cannot be primary.",
                    ),
                },
            )

        if self.is_primary and self.is_deleted:
            raise ValidationError(
                {
                    "is_primary": _(
                        "A deleted contact cannot be primary.",
                    ),
                },
            )

    def __str__(self) -> str:
        """
        Return the contact value.
        """
        return self.value


__all__ = ("Contact",)

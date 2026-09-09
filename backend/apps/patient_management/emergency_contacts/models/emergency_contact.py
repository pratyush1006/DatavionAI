"""
Emergency Contact domain model.

Represents a patient's designated emergency contact within an organization.

The model is intentionally lean:
- persistence
- field validation
- database constraints
- lightweight presentation helpers

Mutation orchestration belongs to workflows and services.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import AuditableModel
from apps.patient_management.emergency_contacts.managers import (
    EmergencyContactManager,
)
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
    validate_priority_order,
)


class EmergencyContact(
    AuditableModel,
):
    """
    Patient emergency contact.

    A patient may have multiple emergency contacts, but only one
    active primary emergency contact at a time.
    """

    objects = EmergencyContactManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
        db_index=True,
        verbose_name=_("Organization"),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
        db_index=True,
        verbose_name=_("Patient"),
    )

    emergency_contact_number = models.CharField(
        max_length=30,
        validators=(validate_emergency_contact_number,),
        verbose_name=_("Emergency Contact Number"),
        help_text=_(
            "System-generated emergency contact identifier.",
        ),
    )

    first_name = models.CharField(
        max_length=100,
        verbose_name=_("First Name"),
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Middle Name"),
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_("Last Name"),
    )

    relationship = models.CharField(
        max_length=50,
        choices=EmergencyContactRelationship.choices,
        verbose_name=_("Relationship"),
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of Birth"),
    )

    mobile_number = models.CharField(
        max_length=20,
        validators=(validate_phone_number,),
        verbose_name=_("Mobile Number"),
    )

    alternate_mobile_number = models.CharField(
        max_length=20,
        blank=True,
        validators=(validate_phone_number,),
        verbose_name=_("Alternate Mobile Number"),
    )

    home_phone = models.CharField(
        max_length=20,
        blank=True,
        validators=(validate_phone_number,),
        verbose_name=_("Home Phone"),
    )

    work_phone = models.CharField(
        max_length=20,
        blank=True,
        validators=(validate_phone_number,),
        verbose_name=_("Work Phone"),
    )

    email = models.EmailField(
        blank=True,
        validators=(validate_email_address,),
        verbose_name=_("Email"),
    )

    preferred_contact_method = models.CharField(
        max_length=20,
        choices=PreferredContactMethod.choices,
        default=PreferredContactMethod.MOBILE,
        verbose_name=_("Preferred Contact Method"),
    )

    address_line_1 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Address Line 1"),
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Address Line 2"),
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("City"),
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("State"),
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Postal Code"),
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Country"),
    )

    is_primary = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Primary"),
    )

    priority_order = models.PositiveSmallIntegerField(
        default=1,
        validators=(validate_priority_order,),
        verbose_name=_("Priority Order"),
    )

    availability = models.CharField(
        max_length=30,
        choices=EmergencyContactAvailability.choices,
        default=EmergencyContactAvailability.ALWAYS,
        verbose_name=_("Availability"),
    )

    status = models.CharField(
        max_length=20,
        choices=EmergencyContactStatus.choices,
        default=EmergencyContactStatus.ACTIVE,
        db_index=True,
        verbose_name=_("Status"),
    )

    is_verified = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Verified"),
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Verified At"),
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Verified By"),
    )

    is_legal_guardian = models.BooleanField(
        default=False,
        verbose_name=_("Legal Guardian"),
    )

    has_medical_power_of_attorney = models.BooleanField(
        default=False,
        verbose_name=_("Medical Power of Attorney"),
    )

    notes = models.TextField(
        blank=True,
        validators=(validate_notes,),
        verbose_name=_("Notes"),
    )

    class Meta:
        verbose_name = _("Emergency Contact")
        verbose_name_plural = _("Emergency Contacts")
        ordering = (
            "priority_order",
            "first_name",
            "last_name",
        )

        constraints = (
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "emergency_contact_number",
                ),
                condition=Q(
                    is_deleted=False,
                ),
                name="uniq_org_emergency_contact_number",
            ),
            models.UniqueConstraint(
                fields=(
                    "patient",
                    "priority_order",
                ),
                condition=Q(
                    is_deleted=False,
                ),
                name="uniq_patient_priority_order",
            ),
            models.UniqueConstraint(
                fields=("patient",),
                condition=Q(
                    is_primary=True,
                    is_deleted=False,
                ),
                name="uniq_primary_patient_emergency_contact",
            ),
        )

        indexes = (
            models.Index(
                fields=(
                    "organization",
                    "patient",
                ),
                name="idx_ec_org_patient",
            ),
            models.Index(
                fields=(
                    "organization",
                    "is_deleted",
                ),
                name="idx_ec_org_deleted",
            ),
            models.Index(
                fields=(
                    "patient",
                    "priority_order",
                ),
                name="idx_ec_patient_priority",
            ),
            models.Index(
                fields=(
                    "patient",
                    "status",
                ),
                name="idx_ec_patient_status",
            ),
            models.Index(
                fields=("status",),
                name="idx_ec_status",
            ),
            models.Index(
                fields=("relationship",),
                name="idx_ec_relationship",
            ),
            models.Index(
                fields=("is_primary",),
                name="idx_ec_primary",
            ),
            models.Index(
                fields=("is_verified",),
                name="idx_ec_verified",
            ),
        )

    @property
    def full_name(
        self,
    ) -> str:
        """
        Return the contact's normalized display name.
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
        return f"{self.emergency_contact_number} - {self.full_name}"


__all__ = ("EmergencyContact",)

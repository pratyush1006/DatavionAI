"""
Patient Family Member model.

Represents an organization-scoped family member associated with the
canonical Patient Management Patient aggregate.
"""

from __future__ import annotations

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.patient_management.family_members.constants import (
    FamilyMemberGender,
    FamilyMemberRelationship,
    FamilyMemberStatus,
)
from apps.patient_management.family_members.managers import (
    DeletedFamilyMemberManager,
    FamilyMemberManager,
)
from apps.patient_management.family_members.validators import (
    validate_date_of_birth,
    validate_email_address,
    validate_family_member_name,
    validate_mobile_number,
    validate_notes,
)
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class FamilyMember(BaseModel):
    """
    Organization-scoped family member belonging to a canonical Patient.

    Operational uniqueness applies only to non-deleted records.
    A patient can have at most one active next of kin.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="family_members",
        verbose_name=_("Organization"),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="family_members",
        verbose_name=_("Patient"),
    )

    family_member_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        editable=False,
        verbose_name=_("Family Member Number"),
    )

    first_name = models.CharField(
        max_length=100,
        validators=[validate_family_member_name],
        verbose_name=_("First Name"),
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Middle Name"),
    )

    last_name = models.CharField(
        max_length=100,
        validators=[validate_family_member_name],
        verbose_name=_("Last Name"),
    )

    relationship = models.CharField(
        max_length=50,
        choices=FamilyMemberRelationship.choices,
        db_index=True,
        verbose_name=_("Relationship"),
    )

    gender = models.CharField(
        max_length=20,
        choices=FamilyMemberGender.choices,
        default=FamilyMemberGender.UNKNOWN,
        verbose_name=_("Gender"),
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        validators=[validate_date_of_birth],
        verbose_name=_("Date of Birth"),
    )

    mobile_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_mobile_number],
        verbose_name=_("Mobile Number"),
    )

    email = models.EmailField(
        blank=True,
        validators=[validate_email_address],
        verbose_name=_("Email"),
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True,
        verbose_name=_("Blood Group"),
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Occupation"),
    )

    address = models.TextField(
        blank=True,
        verbose_name=_("Address"),
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

    is_living = models.BooleanField(
        default=True,
        verbose_name=_("Living"),
    )

    is_emergency_contact = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Emergency Contact"),
    )

    is_next_of_kin = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Next of Kin"),
    )

    notes = models.TextField(
        blank=True,
        validators=[validate_notes],
        verbose_name=_("Notes"),
    )

    status = models.CharField(
        max_length=20,
        choices=FamilyMemberStatus.choices,
        default=FamilyMemberStatus.ACTIVE,
        db_index=True,
        verbose_name=_("Status"),
    )

    objects = FamilyMemberManager()
    deleted_objects = DeletedFamilyMemberManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = _("Family Member")
        verbose_name_plural = _("Family Members")
        ordering = ("first_name", "last_name")
        indexes = [
            models.Index(
                fields=("organization", "patient"),
                name="fm_org_patient_idx",
            ),
            models.Index(
                fields=("organization", "is_deleted"),
                name="fm_org_deleted_idx",
            ),
            models.Index(
                fields=("patient", "relationship"),
                name="fm_patient_relationship_idx",
            ),
            models.Index(
                fields=("patient", "status"),
                name="fm_patient_status_idx",
            ),
            models.Index(
                fields=("patient", "is_next_of_kin"),
                name="fm_patient_next_kin_idx",
            ),
            models.Index(
                fields=("patient", "is_emergency_contact"),
                name="fm_patient_emergency_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "patient",
                    "relationship",
                    "first_name",
                    "last_name",
                ),
                condition=Q(is_deleted=False),
                name="uniq_active_patient_family_member",
            ),
            models.UniqueConstraint(
                fields=("patient",),
                condition=Q(
                    is_next_of_kin=True,
                    is_deleted=False,
                ),
                name="uniq_active_patient_next_of_kin",
            ),
        ]

    @property
    def full_name(self) -> str:
        return " ".join(
            part
            for part in (
                self.first_name,
                self.middle_name,
                self.last_name,
            )
            if part
        )

    def save(self, *args: object, **kwargs: object) -> None:
        self.first_name = (self.first_name or "").strip()
        self.middle_name = (self.middle_name or "").strip()
        self.last_name = (self.last_name or "").strip()
        self.email = (self.email or "").strip().lower()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.full_name} ({self.get_relationship_display()})"


__all__ = ("FamilyMember",)

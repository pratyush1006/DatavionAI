"""
Family Member model.
"""

from __future__ import annotations

from django.db import models
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

__all__ = [
    "FamilyMember",
]


class FamilyMember(BaseModel):
    """
    Stores a patient's family member.
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
        verbose_name=_("Family Member Number"),
    )

    first_name = models.CharField(
        max_length=100,
        validators=[validate_family_member_name],
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
        validators=[validate_family_member_name],
    )

    relationship = models.CharField(
        max_length=50,
        choices=FamilyMemberRelationship.choices,
        db_index=True,
    )

    gender = models.CharField(
        max_length=20,
        choices=FamilyMemberGender.choices,
        default=FamilyMemberGender.UNKNOWN,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        validators=[validate_date_of_birth],
    )

    mobile_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_mobile_number],
    )

    email = models.EmailField(
        blank=True,
        validators=[validate_email_address],
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True,
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
    )

    address = models.TextField(
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

    is_living = models.BooleanField(
        default=True,
    )

    is_emergency_contact = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_next_of_kin = models.BooleanField(
        default=False,
        db_index=True,
    )

    notes = models.TextField(
        blank=True,
        validators=[validate_notes],
    )

    status = models.CharField(
        max_length=20,
        choices=FamilyMemberStatus.choices,
        default=FamilyMemberStatus.ACTIVE,
        db_index=True,
    )

    objects = FamilyMemberManager()
    deleted_objects = DeletedFamilyMemberManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = _("Family Member")
        verbose_name_plural = _("Family Members")
        ordering = (
            "first_name",
            "last_name",
        )
        indexes = [
            models.Index(fields=["organization"]),
            models.Index(fields=["patient"]),
            models.Index(fields=["relationship"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_next_of_kin"]),
            models.Index(fields=["is_emergency_contact"]),
            models.Index(fields=["family_member_number"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "patient",
                    "relationship",
                    "first_name",
                    "last_name",
                ],
                name="unique_patient_family_member",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.get_relationship_display()})"

    @property
    def full_name(self) -> str:
        """
        Return the formatted full name.
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

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Normalize values before saving.
        """
        self.first_name = self.first_name.strip()
        self.middle_name = self.middle_name.strip()
        self.last_name = self.last_name.strip()
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)

"""
Patient relationship domain model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import (
    AllObjectsManager,
    BaseModel,
    DeletedObjectsManager,
)
from apps.patient_management.patients.models import Patient
from apps.patient_management.relationships.constants import (
    RelationshipStatus,
    RelationshipType,
    VerificationStatus,
)
from apps.patient_management.relationships.managers import PatientRelationshipManager
from apps.platform.organizations.models import Organization


class PatientRelationship(BaseModel):
    """
    Relationship between a patient and another patient or an
    external individual/entity.
    """

    objects = PatientRelationshipManager()
    all_objects = AllObjectsManager()
    deleted_objects = DeletedObjectsManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_relationships",
        help_text=_("Organization that owns the relationship."),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="patient_relationships",
        help_text=_("Primary patient."),
    )

    related_patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="related_patient_relationships",
        help_text=_("Related patient, when the relationship is internal."),
    )

    relationship_type = models.CharField(
        max_length=30,
        choices=RelationshipType.choices,
        help_text=_("Type of relationship."),
    )

    relationship_name = models.CharField(
        max_length=150,
        blank=True,
        help_text=_(
            "External person's or entity's relationship name "
            "when related_patient is not supplied."
        ),
    )

    is_primary = models.BooleanField(
        default=False,
        help_text=_("Whether this is the patient's primary relationship."),
    )

    status = models.CharField(
        max_length=20,
        choices=RelationshipStatus.choices,
        default=RelationshipStatus.ACTIVE,
        db_index=True,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )

    effective_from = models.DateField(
        null=True,
        blank=True,
    )

    effective_to = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "patient_relationships"

        verbose_name = _("Patient Relationship")
        verbose_name_plural = _("Patient Relationships")

        ordering = (
            "-is_primary",
            "relationship_type",
            "created_at",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "patient",
                    "related_patient",
                    "relationship_type",
                ),
                condition=models.Q(
                    related_patient__isnull=False,
                    is_active=True,
                ),
                name="uq_patient_relationship_internal",
            ),
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "patient",
                    "relationship_name",
                    "relationship_type",
                ),
                condition=models.Q(
                    related_patient__isnull=True,
                    is_active=True,
                ),
                name="uq_patient_relationship_external",
            ),
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "patient",
                ),
                condition=models.Q(
                    is_primary=True,
                    is_active=True,
                ),
                name="uq_patient_primary_relationship",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "organization",
                    "patient",
                    "status",
                ),
                name="rel_org_pat_status_idx",
            ),
            models.Index(
                fields=(
                    "organization",
                    "related_patient",
                ),
                name="rel_org_related_idx",
            ),
            models.Index(
                fields=(
                    "patient",
                    "relationship_type",
                ),
                name="rel_patient_type_idx",
            ),
            models.Index(
                fields=("verification_status",),
                name="rel_verification_idx",
            ),
        ]

    def clean(self) -> None:
        super().clean()

        if (
            self.related_patient_id
            and self.patient_id
            and self.related_patient_id == self.patient_id
        ):
            raise ValidationError(
                {
                    "related_patient": _(
                        "A patient cannot have a relationship with themselves."
                    )
                }
            )

        if not self.related_patient_id and not self.relationship_name.strip():
            raise ValidationError(
                {
                    "relationship_name": _(
                        "Relationship name is required for an external relationship."
                    )
                }
            )

        if self.effective_from and self.effective_to:
            if self.effective_to < self.effective_from:
                raise ValidationError(
                    {
                        "effective_to": _(
                            "Effective end date cannot be before the start date."
                        )
                    }
                )

    @property
    def is_external(self) -> bool:
        return self.related_patient_id is None

    @property
    def is_verified(self) -> bool:
        return self.verification_status == VerificationStatus.VERIFIED

    def __str__(self) -> str:
        target = (
            str(self.related_patient)
            if self.related_patient_id
            else self.relationship_name
        )
        return f"{self.patient} → {target} ({self.get_relationship_type_display()})"


__all__ = ("PatientRelationship",)

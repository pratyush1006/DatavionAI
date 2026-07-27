"""
Patient Relationship model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.patient_management.relationships.constants import (
    RelationshipSource,
    RelationshipStatus,
    RelationshipType,
    RelationshipVerificationStatus,
)
from apps.patient_management.relationships.managers import (
    PatientRelationshipManager,
)
from apps.patient_management.relationships.validators import (
    validate_relationship_notes,
    validate_relationship_strength,
)
from apps.platform.organizations.models import Organization


class PatientRelationship(BaseModel):
    """
    Represents a relationship between two patients or between
    a patient and an external individual/entity.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_relationships",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="relationships",
    )

    related_patient = models.ForeignKey(
        Patient,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="related_to",
    )

    relationship_type = models.CharField(
        max_length=50,
        choices=RelationshipType.choices,
    )

    relationship_name = models.CharField(
        max_length=255,
        blank=True,
    )

    relationship_strength = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            validate_relationship_strength,
        ],
    )

    status = models.CharField(
        max_length=20,
        choices=RelationshipStatus.choices,
        default=RelationshipStatus.ACTIVE,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=RelationshipVerificationStatus.choices,
        default=RelationshipVerificationStatus.PENDING,
    )

    source = models.CharField(
        max_length=20,
        choices=RelationshipSource.choices,
        default=RelationshipSource.MANUAL,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
        validators=[
            validate_relationship_notes,
        ],
    )

    objects = PatientRelationshipManager()

    class Meta:
        verbose_name = _("Patient Relationship")
        verbose_name_plural = _("Patient Relationships")

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                ],
            ),
            models.Index(
                fields=[
                    "relationship_type",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "verification_status",
                ],
            ),
            models.Index(
                fields=[
                    "is_primary",
                ],
            ),
            models.Index(
                fields=[
                    "related_patient",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "patient",
                    "related_patient",
                    "relationship_type",
                ],
                name="unique_patient_relationship",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        if self.related_patient:
            return (
                f"{self.patient} → "
                f"{self.related_patient} "
                f"({self.get_relationship_type_display()})"
            )

        return (
            f"{self.patient} → "
            f"{self.relationship_name} "
            f"({self.get_relationship_type_display()})"
        )

    @property
    def is_active(
        self,
    ) -> bool:
        """
        Return whether the relationship is active.
        """
        return self.status == RelationshipStatus.ACTIVE

    @property
    def is_verified(
        self,
    ) -> bool:
        """
        Return whether the relationship is verified.
        """
        return self.verification_status == RelationshipVerificationStatus.VERIFIED

    @property
    def is_external_relationship(
        self,
    ) -> bool:
        """
        Return whether this relationship references an
        external individual instead of another patient.
        """
        return self.related_patient_id is None

    def clean(
        self,
    ) -> None:
        """
        Validate the relationship.
        """
        super().clean()

        if self.related_patient and self.related_patient_id == self.patient_id:
            raise ValidationError(
                {
                    "related_patient": _(
                        "A patient cannot have a relationship with themselves.",
                    ),
                },
            )

        if not self.related_patient and not self.relationship_name:
            raise ValidationError(
                {
                    "relationship_name": _(
                        "Relationship name is required for external relationships.",
                    ),
                },
            )

        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError(
                {
                    "end_date": _(
                        "End date cannot be earlier than start date.",
                    ),
                },
            )

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Validate before saving.
        """
        self.full_clean()

        super().save(
            *args,
            **kwargs,
        )

    def activate(
        self,
    ) -> None:
        """
        Activate the relationship.
        """
        self.status = RelationshipStatus.ACTIVE

        self.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

    def deactivate(
        self,
    ) -> None:
        """
        Deactivate the relationship.
        """
        self.status = RelationshipStatus.INACTIVE

        self.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

    def verify(
        self,
    ) -> None:
        """
        Mark the relationship as verified.
        """
        self.verification_status = RelationshipVerificationStatus.VERIFIED

        self.save(
            update_fields=[
                "verification_status",
                "updated_at",
            ],
        )

    def terminate(
        self,
        *,
        end_date=None,
    ) -> None:
        """
        Terminate the relationship.
        """
        from django.utils import timezone

        self.status = RelationshipStatus.TERMINATED
        self.end_date = end_date or timezone.localdate()

        self.save(
            update_fields=[
                "status",
                "end_date",
                "updated_at",
            ],
        )

    def mark_as_primary(
        self,
    ) -> None:
        """
        Mark this relationship as the primary relationship
        for the patient and relationship type.
        """
        type(self).objects.filter(
            patient=self.patient,
            relationship_type=self.relationship_type,
            is_primary=True,
        ).exclude(
            pk=self.pk,
        ).update(
            is_primary=False,
        )

        self.is_primary = True

        self.save(
            update_fields=[
                "is_primary",
                "updated_at",
            ],
        )

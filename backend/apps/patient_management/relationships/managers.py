"""
Custom managers and querysets for Patient Relationships.
"""

from __future__ import annotations

from django.db import models

from apps.patient_management.relationships.constants import (
    RelationshipStatus,
    RelationshipVerificationStatus,
)


class PatientRelationshipQuerySet(models.QuerySet):
    """QuerySet for PatientRelationship."""

    def active(self) -> PatientRelationshipQuerySet:
        return self.filter(
            status=RelationshipStatus.ACTIVE,
        )

    def inactive(self) -> PatientRelationshipQuerySet:
        return self.filter(
            status=RelationshipStatus.INACTIVE,
        )

    def terminated(self) -> PatientRelationshipQuerySet:
        return self.filter(
            status=RelationshipStatus.TERMINATED,
        )

    def verified(self) -> PatientRelationshipQuerySet:
        return self.filter(
            verification_status=RelationshipVerificationStatus.VERIFIED,
        )

    def pending(self) -> PatientRelationshipQuerySet:
        return self.filter(
            verification_status=RelationshipVerificationStatus.PENDING,
        )

    def primary(self) -> PatientRelationshipQuerySet:
        return self.filter(
            is_primary=True,
        )

    def by_organization(
        self,
        organization_id: int,
    ) -> PatientRelationshipQuerySet:
        return self.filter(
            organization_id=organization_id,
        )

    def by_patient(
        self,
        patient_id: int,
    ) -> PatientRelationshipQuerySet:
        return self.filter(
            patient_id=patient_id,
        )

    def by_relationship_type(
        self,
        relationship_type: str,
    ) -> PatientRelationshipQuerySet:
        return self.filter(
            relationship_type=relationship_type,
        )


PatientRelationshipManager = models.Manager.from_queryset(
    PatientRelationshipQuerySet,
)

__all__ = [
    "PatientRelationshipManager",
    "PatientRelationshipQuerySet",
]

"""
Querysets and managers for Patient Relationships.

Query code remains reusable and side-effect free. Tenant/organization
scoping is applied by selectors for API-facing reads.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self
from uuid import UUID

from django.db import models

from apps.patient_management.relationships.constants import (
    RelationshipStatus,
    VerificationStatus,
)

if TYPE_CHECKING:
    pass


class PatientRelationshipQuerySet(models.QuerySet["PatientRelationship"]):
    """Reusable queryset operations for PatientRelationship."""

    def active(self) -> Self:
        return self.filter(
            is_deleted=False,
            is_active=True,
            status=RelationshipStatus.ACTIVE,
        )

    def inactive(self) -> Self:
        return self.filter(
            is_deleted=False,
            is_active=False,
            status=RelationshipStatus.INACTIVE,
        )

    def terminated(self) -> Self:
        return self.filter(
            is_deleted=False,
            status=RelationshipStatus.TERMINATED,
        )

    def verified(self) -> Self:
        return self.filter(
            is_deleted=False,
            verification_status=VerificationStatus.VERIFIED,
        )

    def pending_verification(self) -> Self:
        return self.filter(
            is_deleted=False,
            verification_status=VerificationStatus.PENDING,
        )

    def rejected(self) -> Self:
        return self.filter(
            is_deleted=False,
            verification_status=VerificationStatus.REJECTED,
        )

    def primary(self) -> Self:
        return self.filter(
            is_deleted=False,
            is_active=True,
            is_primary=True,
        )

    def external(self) -> Self:
        return self.filter(
            is_deleted=False,
            related_patient__isnull=True,
        )

    def internal(self) -> Self:
        return self.filter(
            is_deleted=False,
            related_patient__isnull=False,
        )

    def for_patient(self, patient_id: UUID) -> Self:
        return self.filter(
            patient_id=patient_id,
            is_deleted=False,
        )

    def for_organization(self, organization_id: UUID) -> Self:
        return self.filter(
            organization_id=organization_id,
            is_deleted=False,
        )

    def by_type(self, relationship_type: str) -> Self:
        return self.filter(
            relationship_type=relationship_type,
            is_deleted=False,
        )


class PatientRelationshipManager(
    models.Manager.from_queryset(PatientRelationshipQuerySet)
):
    """Default manager exposing non-deleted relationships."""

    def get_queryset(self) -> PatientRelationshipQuerySet:
        return super().get_queryset().filter(is_deleted=False)


__all__ = (
    "PatientRelationshipManager",
    "PatientRelationshipQuerySet",
)

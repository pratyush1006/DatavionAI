"""
QuerySet and manager infrastructure for Patient Identifiers.

The manager provides reusable, organization-aware query primitives.
Business authorization remains in policies and workflow orchestration.
"""

from __future__ import annotations

from typing import Self
from uuid import UUID

from django.db import models

from apps.patient_management.identifiers.constants import (
    IdentifierStatus,
    VerificationStatus,
)


class PatientIdentifierQuerySet(
    models.QuerySet["PatientIdentifier"],
):
    """Reusable queryset operations for patient identifiers."""

    def active(self) -> Self:
        """Return active identifiers."""
        return self.filter(
            status=IdentifierStatus.ACTIVE,
        )

    def inactive(self) -> Self:
        """Return inactive identifiers."""
        return self.filter(
            status=IdentifierStatus.INACTIVE,
        )

    def revoked(self) -> Self:
        """Return revoked identifiers."""
        return self.filter(
            status=IdentifierStatus.REVOKED,
        )

    def verified(self) -> Self:
        """Return verified identifiers."""
        return self.filter(
            verification_status=VerificationStatus.VERIFIED,
        )

    def pending(self) -> Self:
        """Return identifiers awaiting verification."""
        return self.filter(
            verification_status=VerificationStatus.PENDING,
        )

    def rejected(self) -> Self:
        """Return rejected identifiers."""
        return self.filter(
            verification_status=VerificationStatus.REJECTED,
        )

    def expired(self) -> Self:
        """Return identifiers marked expired."""
        return self.filter(
            status=IdentifierStatus.EXPIRED,
        )

    def primary(self) -> Self:
        """Return primary identifiers."""
        return self.filter(
            is_primary=True,
        )

    def by_organization(
        self,
        organization_id: UUID,
    ) -> Self:
        """Restrict identifiers to an organization."""
        return self.filter(
            organization_id=organization_id,
        )

    def by_patient(
        self,
        patient_id: UUID,
    ) -> Self:
        """Restrict identifiers to a patient."""
        return self.filter(
            patient_id=patient_id,
        )

    def by_identifier_type(
        self,
        identifier_type: str,
    ) -> Self:
        """Restrict identifiers to an identifier type."""
        return self.filter(
            identifier_type=identifier_type,
        )

    def for_patient(
        self,
        *,
        organization_id: UUID,
        patient_id: UUID,
    ) -> Self:
        """
        Return identifiers for a patient inside an organization.

        Organization scoping is deliberately retained even though the
        patient relation itself is organization-owned.
        """
        return self.filter(
            organization_id=organization_id,
            patient_id=patient_id,
        )

    def with_relations(self) -> Self:
        """Optimize common API reads."""
        return self.select_related(
            "organization",
            "patient",
            "verified_by",
        )

    def ordered(self) -> Self:
        """Apply canonical identifier ordering."""
        return self.order_by(
            "-is_primary",
            "priority",
            "identifier_type",
            "created_at",
        )


class PatientIdentifierManager(models.Manager.from_queryset(PatientIdentifierQuerySet)):
    """Concrete migration-serializable manager class."""


__all__ = (
    "PatientIdentifierManager",
    "PatientIdentifierQuerySet",
)

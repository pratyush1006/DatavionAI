# apps/patient_management/identifiers/managers.py

"""
Custom managers and querysets for patient identifiers.
"""

from __future__ import annotations

from django.db import models


class PatientIdentifierQuerySet(models.QuerySet):
    """QuerySet for PatientIdentifier."""

    def active(self) -> PatientIdentifierQuerySet:
        return self.filter(status="ACTIVE")

    def inactive(self) -> PatientIdentifierQuerySet:
        return self.filter(status="INACTIVE")

    def revoked(self) -> PatientIdentifierQuerySet:
        return self.filter(status="REVOKED")

    def verified(self) -> PatientIdentifierQuerySet:
        return self.filter(verification_status="VERIFIED")

    def pending(self) -> PatientIdentifierQuerySet:
        return self.filter(verification_status="PENDING")

    def primary(self) -> PatientIdentifierQuerySet:
        return self.filter(is_primary=True)

    def by_organization(
        self,
        organization_id: int,
    ) -> PatientIdentifierQuerySet:
        return self.filter(
            organization_id=organization_id,
        )

    def by_patient(
        self,
        patient_id: int,
    ) -> PatientIdentifierQuerySet:
        return self.filter(
            patient_id=patient_id,
        )

    def by_identifier_type(
        self,
        identifier_type: str,
    ) -> PatientIdentifierQuerySet:
        return self.filter(
            identifier_type=identifier_type,
        )


PatientIdentifierManager = models.Manager.from_queryset(
    PatientIdentifierQuerySet,
)

__all__ = [
    "PatientIdentifierManager",
    "PatientIdentifierQuerySet",
]

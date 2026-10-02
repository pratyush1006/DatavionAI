"""Managers and querysets for Patient Documents."""

from __future__ import annotations

from apps.core.models import (
    SoftDeleteManager,
    SoftDeleteQuerySet,
)


class PatientDocumentQuerySet(
    SoftDeleteQuerySet["PatientDocument"],
):
    """Query helpers for tenant-scoped patient documents."""

    def for_organization(
        self,
        organization_id,
    ) -> PatientDocumentQuerySet:
        """Return documents belonging to one organization."""
        return self.filter(
            organization_id=organization_id,
        )

    def for_patient(
        self,
        patient_id,
    ) -> PatientDocumentQuerySet:
        """Return documents belonging to one patient."""
        return self.filter(
            patient_id=patient_id,
        )

    def active(
        self,
    ) -> PatientDocumentQuerySet:
        """Return active documents."""
        return self.filter(
            status="active",
            is_active=True,
        )

    def archived(
        self,
    ) -> PatientDocumentQuerySet:
        """Return archived documents."""
        return self.filter(
            status="archived",
        )

    def by_category(
        self,
        category: str,
    ) -> PatientDocumentQuerySet:
        """Filter documents by category."""
        return self.filter(
            category=category,
        )


class PatientDocumentManager(
    SoftDeleteManager.from_queryset(
        PatientDocumentQuerySet,
    ),
):
    """Default manager that hides soft-deleted documents."""


__all__ = (
    "PatientDocumentManager",
    "PatientDocumentQuerySet",
)

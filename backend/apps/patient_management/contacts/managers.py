"""
Custom managers and querysets for patient contacts.
"""

from __future__ import annotations

from uuid import UUID

from django.db import models

from apps.patient_management.contacts.constants import ContactStatus


class ContactQuerySet(models.QuerySet):
    """
    QuerySet for Patient Contact.

    These helpers provide reusable filtering primitives. Authorization and
    organization isolation remain the responsibility of selectors/policies.
    """

    def active(self) -> ContactQuerySet:
        """Return active contacts."""
        return self.filter(
            status=ContactStatus.ACTIVE,
        )

    def inactive(self) -> ContactQuerySet:
        """Return inactive contacts."""
        return self.filter(
            status=ContactStatus.INACTIVE,
        )

    def verified(self) -> ContactQuerySet:
        """Return verified contacts."""
        return self.filter(
            status=ContactStatus.VERIFIED,
        )

    def unverified(self) -> ContactQuerySet:
        """Return unverified contacts."""
        return self.filter(
            status=ContactStatus.UNVERIFIED,
        )

    def primary(self) -> ContactQuerySet:
        """Return primary contacts."""
        return self.filter(
            is_primary=True,
        )

    def preferred(self) -> ContactQuerySet:
        """Return preferred contacts."""
        return self.filter(
            is_preferred=True,
        )

    def for_organization(
        self,
        organization_id: UUID,
    ) -> ContactQuerySet:
        """Return contacts belonging to one organization."""
        return self.filter(
            organization_id=organization_id,
        )

    def for_patient(
        self,
        patient_id: UUID,
    ) -> ContactQuerySet:
        """Return contacts belonging to one patient."""
        return self.filter(
            patient_id=patient_id,
        )

    def for_patient_in_organization(
        self,
        *,
        organization_id: UUID,
        patient_id: UUID,
    ) -> ContactQuerySet:
        """
        Return contacts for a patient within a specific organization.

        This helper makes the ownership boundary explicit for callers that
        need both identifiers.
        """
        return self.filter(
            organization_id=organization_id,
            patient_id=patient_id,
        )


ContactManager = models.Manager.from_queryset(
    ContactQuerySet,
)


__all__ = (
    "ContactManager",
    "ContactQuerySet",
)

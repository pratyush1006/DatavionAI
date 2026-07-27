"""
Custom managers and querysets for patient contacts.
"""

from __future__ import annotations

from django.db import models

from apps.patient_management.contacts.constants import (
    ContactStatus,
)


class ContactQuerySet(models.QuerySet):
    """QuerySet for Contact."""

    def active(self) -> ContactQuerySet:
        return self.filter(
            status=ContactStatus.ACTIVE,
        )

    def verified(self) -> ContactQuerySet:
        return self.filter(
            status=ContactStatus.VERIFIED,
        )

    def primary(self) -> ContactQuerySet:
        return self.filter(
            is_primary=True,
        )

    def preferred(self) -> ContactQuerySet:
        return self.filter(
            is_preferred=True,
        )

    def for_organization(
        self,
        organization_id: int,
    ) -> ContactQuerySet:
        return self.filter(
            organization_id=organization_id,
        )

    def for_patient(
        self,
        patient_id: int,
    ) -> ContactQuerySet:
        return self.filter(
            patient_id=patient_id,
        )


ContactManager = models.Manager.from_queryset(
    ContactQuerySet,
)

__all__ = [
    "ContactManager",
    "ContactQuerySet",
]

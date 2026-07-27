"""
Custom managers and querysets for patient addresses.
"""

from __future__ import annotations

from django.db import models

from apps.patient_management.addresses.constants import (
    AddressStatus,
)


class AddressQuerySet(models.QuerySet):
    """QuerySet for Address."""

    def active(self) -> AddressQuerySet:
        return self.filter(
            status=AddressStatus.ACTIVE,
        )

    def verified(self) -> AddressQuerySet:
        return self.filter(
            status=AddressStatus.VERIFIED,
        )

    def primary(self) -> AddressQuerySet:
        return self.filter(
            is_primary=True,
        )

    def for_organization(
        self,
        organization_id: int,
    ) -> AddressQuerySet:
        return self.filter(
            organization_id=organization_id,
        )

    def for_patient(
        self,
        patient_id: int,
    ) -> AddressQuerySet:
        return self.filter(
            patient_id=patient_id,
        )


AddressManager = models.Manager.from_queryset(
    AddressQuerySet,
)

__all__ = [
    "AddressManager",
    "AddressQuerySet",
]

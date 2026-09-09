"""
Querysets and managers for Patient Addresses.
"""

from __future__ import annotations

from uuid import UUID

from django.db import models

from apps.patient_management.addresses.constants import (
    AddressStatus,
)


class AddressQuerySet(
    models.QuerySet,
):
    """
    QuerySet for Patient Address.
    """

    def active(
        self,
    ) -> AddressQuerySet:
        return self.filter(
            status=AddressStatus.ACTIVE,
        )

    def inactive(
        self,
    ) -> AddressQuerySet:
        return self.filter(
            status=AddressStatus.INACTIVE,
        )

    def verified(
        self,
    ) -> AddressQuerySet:
        return self.filter(
            status=AddressStatus.VERIFIED,
        )

    def unverified(
        self,
    ) -> AddressQuerySet:
        return self.filter(
            status=AddressStatus.UNVERIFIED,
        )

    def primary(
        self,
    ) -> AddressQuerySet:
        return self.filter(
            is_primary=True,
        )

    def by_organization(
        self,
        organization_id: UUID | str,
    ) -> AddressQuerySet:
        return self.filter(
            organization_id=organization_id,
        )

    def by_patient(
        self,
        patient_id: UUID | str,
    ) -> AddressQuerySet:
        return self.filter(
            patient_id=patient_id,
        )

    def by_type(
        self,
        address_type: str,
    ) -> AddressQuerySet:
        return self.filter(
            address_type=address_type,
        )

    def search(
        self,
        query: str,
    ) -> AddressQuerySet:
        query = query.strip()

        if not query:
            return self

        return self.filter(
            models.Q(
                line_1__icontains=query,
            )
            | models.Q(
                line_2__icontains=query,
            )
            | models.Q(
                city__icontains=query,
            )
            | models.Q(
                state__icontains=query,
            )
            | models.Q(
                country__icontains=query,
            )
            | models.Q(
                postal_code__icontains=query,
            )
            | models.Q(
                patient__first_name__icontains=query,
            )
            | models.Q(
                patient__last_name__icontains=query,
            )
            | models.Q(
                patient__mrn__icontains=query,
            )
        ).distinct()

    def ordered(
        self,
    ) -> AddressQuerySet:
        return self.order_by(
            "-is_primary",
            "address_type",
            "city",
            "-created_at",
        )

    def with_relations(
        self,
    ) -> AddressQuerySet:
        return self.select_related(
            "organization",
            "patient",
        )


AddressManager = models.Manager.from_queryset(
    AddressQuerySet,
)


__all__ = (
    "AddressManager",
    "AddressQuerySet",
)

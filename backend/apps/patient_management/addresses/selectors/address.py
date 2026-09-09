"""
Read-side selectors for Patient Addresses.

Selectors are strictly read-only and always require an explicit
organization boundary for tenant-safe access.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.addresses.models import Address
from apps.platform.organizations.models import Organization


class AddressSelector:
    """
    Read-only selector for Patient Address data.

    All selector access is explicitly organization-scoped to prevent
    cross-tenant data exposure.
    """

    @staticmethod
    def queryset(
        *,
        organization: Organization,
    ) -> QuerySet[Address]:
        """
        Return the tenant-scoped Address queryset.

        The organization boundary is mandatory. Callers must never
        retrieve addresses without an explicit organization scope.
        """
        return Address.objects.with_relations().filter(
            organization_id=organization.pk,
        )

    @staticmethod
    def get(
        *,
        address_id: UUID,
        organization: Organization,
    ) -> Address:
        """
        Retrieve a single address within the organization boundary.
        """
        return get_object_or_404(
            AddressSelector.queryset(
                organization=organization,
            ),
            pk=address_id,
        )

    @staticmethod
    def get_by_value(
        *,
        organization: Organization,
        address_type: str,
        line_1: str,
        postal_code: str,
    ) -> Address:
        """
        Retrieve an address matching the supplied identifying values
        within the organization boundary.
        """
        return get_object_or_404(
            AddressSelector.queryset(
                organization=organization,
            ),
            address_type=address_type,
            line_1=line_1,
            postal_code=postal_code,
        )

    @staticmethod
    def list_by_patient(
        *,
        organization: Organization,
        patient_id: UUID,
    ) -> QuerySet[Address]:
        """
        List all addresses belonging to a patient within the organization.
        """
        return (
            AddressSelector.queryset(
                organization=organization,
            )
            .filter(
                patient_id=patient_id,
            )
            .ordered()
        )

    @staticmethod
    def list_primary(
        *,
        organization: Organization,
        patient_id: UUID,
        address_type: str | None = None,
    ) -> QuerySet[Address]:
        """
        List primary addresses for a patient within the organization.

        When address_type is supplied, only the primary address for that
        address type is returned.
        """
        queryset = AddressSelector.queryset(
            organization=organization,
        ).filter(
            patient_id=patient_id,
            is_primary=True,
        )

        if address_type:
            queryset = queryset.filter(
                address_type=address_type,
            )

        return queryset.ordered()


__all__ = ("AddressSelector",)

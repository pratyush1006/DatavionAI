"""
Read-side selectors for Patient Contacts.

Selectors are read-only and always require an explicit organization
boundary for tenant-safe access.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.contacts.models import Contact
from apps.platform.organizations.models import Organization


class ContactSelector:
    """
    Read-only selector for Patient Contact data.

    Every access path is explicitly organization-scoped.
    """

    @staticmethod
    def queryset(
        *,
        organization: Organization,
    ) -> QuerySet[Contact]:
        """
        Return a tenant-scoped contact queryset.
        """
        return Contact.objects.select_related(
            "organization",
            "patient",
        ).filter(
            organization_id=organization.pk,
        )

    @staticmethod
    def get(
        *,
        contact_id: UUID,
        organization: Organization,
    ) -> Contact:
        """
        Retrieve a single contact inside the organization boundary.
        """
        return get_object_or_404(
            ContactSelector.queryset(
                organization=organization,
            ),
            pk=contact_id,
        )

    @staticmethod
    def get_by_value(
        *,
        organization: Organization,
        contact_type: str,
        value: str,
    ) -> Contact:
        """
        Retrieve a contact by type and normalized value.
        """
        return get_object_or_404(
            ContactSelector.queryset(
                organization=organization,
            ),
            contact_type=contact_type,
            value=value,
        )

    @staticmethod
    def list_by_patient(
        *,
        organization: Organization,
        patient_id: UUID,
    ) -> QuerySet[Contact]:
        """
        Return all contacts for a patient inside the organization boundary.
        """
        return (
            ContactSelector.queryset(
                organization=organization,
            )
            .filter(
                patient_id=patient_id,
            )
            .order_by(
                "-is_primary",
                "-is_preferred",
                "contact_type",
                "created_at",
            )
        )

    @staticmethod
    def list_primary(
        *,
        organization: Organization,
        patient_id: UUID,
        contact_type: str | None = None,
    ) -> QuerySet[Contact]:
        """
        Return primary contacts for a patient.

        When contact_type is supplied, results are restricted to that type.
        """
        queryset = ContactSelector.queryset(
            organization=organization,
        ).filter(
            patient_id=patient_id,
            is_primary=True,
        )

        if contact_type:
            queryset = queryset.filter(
                contact_type=contact_type,
            )

        return queryset.order_by(
            "contact_type",
            "created_at",
        )

    @staticmethod
    def get_primary(
        *,
        organization: Organization,
        patient_id: UUID,
        contact_type: str,
    ) -> Contact | None:
        """
        Return the primary contact for a patient and contact type.
        """
        return (
            ContactSelector.queryset(
                organization=organization,
            )
            .filter(
                patient_id=patient_id,
                contact_type=contact_type,
                is_primary=True,
            )
            .first()
        )


__all__ = ("ContactSelector",)

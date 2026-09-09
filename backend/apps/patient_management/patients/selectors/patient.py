"""
Patient Core selectors.

Selectors are read-only.

They centralize:
- tenant scoping,
- organization scoping,
- filtering,
- searching,
- ordering,
- active/deleted visibility.

No mutation belongs here.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.patients.constants import (
    PatientStatus,
)
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class PatientSelector:
    """
    Read-only Patient queries.
    """

    @staticmethod
    def queryset() -> QuerySet[Patient]:
        """
        Return the canonical Patient queryset.
        """
        return Patient.objects.select_related(
            "organization",
        )

    @staticmethod
    def list(
        *,
        organization: Organization | None = None,
    ) -> QuerySet[Patient]:
        """
        Return patients optionally restricted to an organization.
        """
        queryset = PatientSelector.queryset()

        if organization is not None:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset

    @staticmethod
    def get(
        *,
        patient_id: UUID,
        organization: Organization | None = None,
        tenant_id: UUID | None = None,
    ) -> Patient:
        """
        Return one patient with explicit tenant/organization isolation.
        """
        queryset = PatientSelector.queryset()

        if tenant_id is not None:
            queryset = queryset.filter(
                organization__tenant_id=tenant_id,
            )

        if organization is not None:
            queryset = queryset.filter(
                organization=organization,
            )

        return get_object_or_404(
            queryset,
            pk=patient_id,
        )

    @staticmethod
    def get_by_mrn(
        *,
        organization: Organization,
        mrn: str,
    ) -> Patient:
        """
        Return a patient by MRN within an organization.
        """
        return get_object_or_404(
            PatientSelector.queryset(),
            organization=organization,
            mrn=mrn.strip().upper(),
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Patient]:
        """
        Return all visible patients belonging to an organization.
        """
        return PatientSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_active(
        *,
        organization: Organization,
    ) -> QuerySet[Patient]:
        """
        Return active patients for an organization.
        """
        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            status=PatientStatus.ACTIVE,
            is_active=True,
        )

    @staticmethod
    def list_inactive(
        *,
        organization: Organization,
    ) -> QuerySet[Patient]:
        """
        Return inactive patients for an organization.
        """
        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            status=PatientStatus.INACTIVE,
        )

    @staticmethod
    def list_archived(
        *,
        organization: Organization,
    ) -> QuerySet[Patient]:
        """
        Return archived patients for an organization.
        """
        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            status=PatientStatus.ARCHIVED,
        )

    @staticmethod
    def search(
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[Patient]:
        """
        Search patients inside one organization.
        """
        normalized_query = query.strip()

        if not normalized_query:
            return PatientSelector.list_by_organization(
                organization=organization,
            )

        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            Q(mrn__icontains=normalized_query)
            | Q(first_name__icontains=normalized_query)
            | Q(middle_name__icontains=normalized_query)
            | Q(last_name__icontains=normalized_query)
            | Q(preferred_name__icontains=normalized_query)
            | Q(phone__icontains=normalized_query)
            | Q(email__icontains=normalized_query),
        )


__all__ = ("PatientSelector",)

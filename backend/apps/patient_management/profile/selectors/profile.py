"""
Patient Profile selectors.

Read-only, organization-scoped query operations.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.profile.models import (
    PatientProfile,
)
from apps.platform.organizations.models import (
    Organization,
)


class ProfileSelector:
    """
    Read-only queries for patient profiles.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientProfile]:
        """
        Return the base optimized queryset.
        """

        return PatientProfile.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        profile_id: UUID,
        organization: Organization | None = None,
        tenant_id: UUID | None = None,
    ) -> PatientProfile:
        """
        Resolve a profile with optional organization/tenant boundaries.
        """

        queryset = ProfileSelector.queryset()

        if organization is not None:
            queryset = queryset.filter(
                organization_id=organization.pk,
            )

        if tenant_id is not None:
            queryset = queryset.filter(
                organization__tenant_id=tenant_id,
            )

        return get_object_or_404(
            queryset,
            pk=profile_id,
        )

    @staticmethod
    def get_for_patient(
        *,
        patient_id: UUID,
        organization: Organization | None = None,
        tenant_id: UUID | None = None,
    ) -> PatientProfile:
        """
        Resolve a profile for a patient with tenant boundaries.
        """

        queryset = ProfileSelector.queryset()

        if organization is not None:
            queryset = queryset.filter(
                organization_id=organization.pk,
            )

        if tenant_id is not None:
            queryset = queryset.filter(
                organization__tenant_id=tenant_id,
            )

        return get_object_or_404(
            queryset,
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[PatientProfile]:
        """
        Return profiles belonging to an organization.
        """

        return ProfileSelector.queryset().filter(
            organization_id=organization.pk,
        )


__all__ = ("ProfileSelector",)

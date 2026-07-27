"""
Patient selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.clinical.patients.constants import PatientStatus
from apps.clinical.patients.models import Patient
from apps.platform.organizations.models import Organization


class PatientSelector:
    """
    Read-only queries for patients.

    This selector centralizes all patient retrieval logic.
    No write operations should be implemented here.
    """

    @staticmethod
    def queryset() -> QuerySet[Patient]:
        """
        Return the base patient queryset.
        """

        return Patient.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[Patient]:
        """
        Return all patients.
        """

        return PatientSelector.queryset()

    @staticmethod
    def get(
        *,
        patient_id: UUID,
    ) -> Patient:
        """
        Return a patient by identifier.
        """

        return get_object_or_404(
            PatientSelector.queryset(),
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
            mrn=mrn,
        )

    @staticmethod
    def search(
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[Patient]:
        """
        Search patients within an organization.
        """

        return (
            PatientSelector.queryset()
            .filter(
                organization=organization,
            )
            .filter(
                Q(
                    first_name__icontains=query,
                )
                | Q(
                    middle_name__icontains=query,
                )
                | Q(
                    last_name__icontains=query,
                )
                | Q(
                    preferred_name__icontains=query,
                )
                | Q(
                    mrn__icontains=query,
                )
                | Q(
                    phone__icontains=query,
                )
                | Q(
                    email__icontains=query,
                ),
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Patient]:
        """
        Return all patients belonging to an organization.
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
        Return active patients.
        """

        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            status=PatientStatus.ACTIVE,
        )

    @staticmethod
    def list_inactive(
        *,
        organization: Organization,
    ) -> QuerySet[Patient]:
        """
        Return inactive patients.
        """

        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            status=PatientStatus.INACTIVE,
        )

    @staticmethod
    def list_deceased(
        *,
        organization: Organization,
    ) -> QuerySet[Patient]:
        """
        Return deceased patients.
        """

        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            status=PatientStatus.DECEASED,
        )

    @staticmethod
    def list_archived(
        *,
        organization: Organization,
    ) -> QuerySet[Patient]:
        """
        Return archived patients.
        """

        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            status=PatientStatus.ARCHIVED,
        )

    @staticmethod
    def list_by_phone(
        *,
        organization: Organization,
        phone: str,
    ) -> QuerySet[Patient]:
        """
        Return patients matching a phone number.
        """

        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            phone=phone,
        )

    @staticmethod
    def list_by_email(
        *,
        organization: Organization,
        email: str,
    ) -> QuerySet[Patient]:
        """
        Return patients matching an email address.
        """

        return PatientSelector.list_by_organization(
            organization=organization,
        ).filter(
            email__iexact=email,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        patient_id: UUID,
    ) -> bool:
        """
        Determine whether a patient exists.
        """

        return (
            PatientSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=patient_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of patients within an organization.
        """

        return PatientSelector.list_by_organization(
            organization=organization,
        ).count()

    @staticmethod
    def paginated(
        *,
        organization: Organization,
    ) -> QuerySet[Patient]:
        """
        Return the base queryset for paginated patient listings.
        Pagination is handled by the API layer.
        """

        return PatientSelector.list_by_organization(
            organization=organization,
        )


# ---------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------

get_patients = PatientSelector.list

get_patient_by_id = PatientSelector.get

get_organization_patients = PatientSelector.list_by_organization


__all__ = [
    "PatientSelector",
    "get_organization_patients",
    "get_patient_by_id",
    "get_patients",
]

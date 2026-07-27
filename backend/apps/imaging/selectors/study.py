"""
Imaging study selector.
"""

from __future__ import annotations

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.imaging.models import Study
from apps.platform.organizations.models import Organization


class StudySelector:
    """
    Read-only queries for imaging studies.
    """

    @staticmethod
    def queryset() -> QuerySet[Study]:
        """
        Return the base study queryset.
        """

        return Study.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def list() -> QuerySet[Study]:
        """
        Return all studies.
        """

        return StudySelector.queryset()

    @staticmethod
    def get(
        *,
        study_id: str,
    ) -> Study:
        """
        Return a study by identifier.
        """

        return get_object_or_404(
            StudySelector.queryset(),
            pk=study_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: str,
    ) -> QuerySet[Study]:
        """
        Return all studies for a patient.
        """

        return StudySelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Study]:
        """
        Return all studies belonging to an organization.
        """

        return StudySelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_by_modality(
        *,
        modality: str,
    ) -> QuerySet[Study]:
        """
        Return all studies for a given modality.
        """

        return StudySelector.queryset().filter(
            modality=modality,
        )

    @staticmethod
    def search(
        *,
        query: str,
    ) -> QuerySet[Study]:
        """
        Search studies by description, referring physician, or accession number.
        """

        return StudySelector.queryset().filter(
            Q(
                study_description__icontains=query,
            )
            | Q(
                referring_physician__icontains=query,
            )
            | Q(
                accession_number__icontains=query,
            )
            | Q(
                study_instance_uid__icontains=query,
            ),
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of studies within an organization.
        """

        return StudySelector.list_by_organization(
            organization=organization,
        ).count()


__all__ = [
    "StudySelector",
]

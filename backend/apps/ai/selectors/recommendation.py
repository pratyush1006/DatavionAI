"""
Recommendation selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.ai.models import Recommendation
from apps.platform.organizations.models import Organization


class RecommendationSelector:
    """
    Read-only queries for recommendations.

    This selector centralizes all recommendation retrieval logic.
    No write operations should be implemented here.
    """

    @staticmethod
    def queryset() -> QuerySet[Recommendation]:
        """
        Return the base recommendation queryset.
        """

        return Recommendation.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def list() -> QuerySet[Recommendation]:
        """
        Return all recommendations.
        """

        return RecommendationSelector.queryset()

    @staticmethod
    def get(
        *,
        recommendation_id: UUID,
    ) -> Recommendation:
        """
        Return a recommendation by identifier.
        """

        return get_object_or_404(
            RecommendationSelector.queryset(),
            pk=recommendation_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[Recommendation]:
        """
        Return recommendations for a specific patient.
        """

        return RecommendationSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Recommendation]:
        """
        Return recommendations belonging to an organization.
        """

        return RecommendationSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_active(
        *,
        organization: Organization,
    ) -> QuerySet[Recommendation]:
        """
        Return active recommendations for an organization.
        """

        return RecommendationSelector.list_by_organization(
            organization=organization,
        ).filter(
            status="pending",
        )

    @staticmethod
    def search(
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[Recommendation]:
        """
        Search recommendations within an organization.
        """

        return (
            RecommendationSelector.queryset()
            .filter(
                organization=organization,
            )
            .filter(
                Q(
                    title__icontains=query,
                )
                | Q(
                    description__icontains=query,
                )
                | Q(
                    recommendation_type__icontains=query,
                )
            )
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of recommendations within an organization.
        """

        return RecommendationSelector.list_by_organization(
            organization=organization,
        ).count()


__all__ = [
    "RecommendationSelector",
]

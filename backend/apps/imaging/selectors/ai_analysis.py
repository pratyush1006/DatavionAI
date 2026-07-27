"""
AI analysis selector.
"""

from __future__ import annotations

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.imaging.models import AIAnalysis
from apps.platform.organizations.models import Organization


class AIAnalysisSelector:
    """
    Read-only queries for AI analyses.
    """

    @staticmethod
    def queryset() -> QuerySet[AIAnalysis]:
        """
        Return the base AI analysis queryset.
        """

        return AIAnalysis.objects.select_related(
            "study",
            "ai_model",
            "reviewed_by",
        )

    @staticmethod
    def list() -> QuerySet[AIAnalysis]:
        """
        Return all AI analyses.
        """

        return AIAnalysisSelector.queryset()

    @staticmethod
    def get(
        *,
        analysis_id: str,
    ) -> AIAnalysis:
        """
        Return an AI analysis by identifier.
        """

        return get_object_or_404(
            AIAnalysisSelector.queryset(),
            pk=analysis_id,
        )

    @staticmethod
    def list_by_study(
        *,
        study_id: str,
    ) -> QuerySet[AIAnalysis]:
        """
        Return all AI analyses for a given study.
        """

        return AIAnalysisSelector.queryset().filter(
            study_id=study_id,
        )

    @staticmethod
    def list_by_model(
        *,
        ai_model_id: str,
    ) -> QuerySet[AIAnalysis]:
        """
        Return all AI analyses for a given AI model.
        """

        return AIAnalysisSelector.queryset().filter(
            ai_model_id=ai_model_id,
        )

    @staticmethod
    def list_unreviewed() -> QuerySet[AIAnalysis]:
        """
        Return all unreviewed AI analyses.
        """

        return AIAnalysisSelector.queryset().filter(
            is_reviewed=False,
        )

    @staticmethod
    def search(
        *,
        query: str,
    ) -> QuerySet[AIAnalysis]:
        """
        Search AI analyses by analysis type or result.
        """

        return AIAnalysisSelector.queryset().filter(
            Q(
                analysis_type__icontains=query,
            )
            | Q(
                result__icontains=query,
            ),
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of AI analyses within an organization.
        """

        return (
            AIAnalysisSelector.queryset()
            .filter(
                study__organization=organization,
            )
            .count()
        )


__all__ = [
    "AIAnalysisSelector",
]

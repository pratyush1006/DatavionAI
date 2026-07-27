"""
AI analysis service.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.imaging.models import AIAnalysis
from apps.platform.accounts.models import User


class AIAnalysisService:
    """Application service responsible for AI analysis lifecycle operations."""

    """
    Application service responsible for AI analysis write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> AIAnalysis:
        """
        Create a new AI analysis.
        """

        analysis = AIAnalysis(
            **validated_data,
        )

        analysis.full_clean()

        analysis.save()

        return analysis

    @staticmethod
    @transaction.atomic
    def review(
        *,
        instance: AIAnalysis,
        reviewed_by: Any,
        validated_data: Mapping[str, Any] | None = None,
    ) -> AIAnalysis:
        """
        Mark an AI analysis as reviewed.
        """

        instance.is_reviewed = True
        instance.reviewed_by = reviewed_by
        instance.reviewed_at = timezone.now()

        if validated_data:
            for field, value in validated_data.items():
                setattr(
                    instance,
                    field,
                    value,
                )

        instance.full_clean()

        instance.save(
            update_fields=[
                "is_reviewed",
                "reviewed_by",
                "reviewed_at",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: AIAnalysis,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> AIAnalysis:
        """Update an AI analysis."""

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.full_clean()
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[AIAnalysis]:
        """
        Create multiple AI analyses.
        """

        analyses: list[AIAnalysis] = []

        for validated_data in validated_data_list:
            analysis = AIAnalysis(
                **validated_data,
            )

            analysis.full_clean()

            analysis.save()

            analyses.append(analysis)

        return analyses


__all__ = [
    "AIAnalysisService",
]

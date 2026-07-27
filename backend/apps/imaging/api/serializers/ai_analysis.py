"""
AI analysis serializers for the Imaging application.
"""

from __future__ import annotations

from apps.imaging.api.serializers.fields import (
    AI_ANALYSIS_DETAIL_FIELDS,
    AI_ANALYSIS_LIST_FIELDS,
    AI_ANALYSIS_READ_ONLY_FIELDS,
    AI_ANALYSIS_UPDATE_FIELDS,
    AI_ANALYSIS_WRITE_FIELDS,
)
from apps.imaging.models import AIAnalysis
from apps.imaging.services import AIAnalysisService


class AIAnalysisBaseSerializer:
    """
    Base serializer mixin for AIAnalysis serializers.
    """

    class Meta:
        model = AIAnalysis
        fields = ()


class AIAnalysisSerializer(
    AIAnalysisBaseSerializer,
):
    """
    Generic AIAnalysis serializer.
    """

    class Meta(
        AIAnalysisBaseSerializer.Meta,
    ):
        fields = (
            "id",
            "study",
            "ai_model",
            "analysis_type",
            "input_image_ids",
            "result",
            "confidence_score",
            "findings",
            "is_reviewed",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        )


class AIAnalysisCreateSerializer(
    AIAnalysisBaseSerializer,
):
    """
    Serializer used for creating AI analyses.
    """

    class Meta(
        AIAnalysisBaseSerializer.Meta,
    ):
        fields = AI_ANALYSIS_WRITE_FIELDS
        read_only_fields = AI_ANALYSIS_READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create an AI analysis.
        """

        return AIAnalysisService.create(
            validated_data=validated_data,
        )


class AIAnalysisUpdateSerializer(
    AIAnalysisBaseSerializer,
):
    """
    Serializer used for updating AI analyses.
    """

    class Meta(
        AIAnalysisBaseSerializer.Meta,
    ):
        fields = AI_ANALYSIS_UPDATE_FIELDS
        read_only_fields = AI_ANALYSIS_READ_ONLY_FIELDS

    def update(
        self,
        instance: AIAnalysis,
        validated_data: dict[str, object],
    ) -> AIAnalysis:
        """
        Update an AI analysis.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance


class AIAnalysisListSerializer(
    AIAnalysisBaseSerializer,
):
    """
    Serializer used for listing AI analyses.
    """

    class Meta(
        AIAnalysisBaseSerializer.Meta,
    ):
        fields = AI_ANALYSIS_LIST_FIELDS
        read_only_fields = AI_ANALYSIS_READ_ONLY_FIELDS


class AIAnalysisDetailSerializer(
    AIAnalysisBaseSerializer,
):
    """
    Serializer used for retrieving AI analysis details.
    """

    class Meta(
        AIAnalysisBaseSerializer.Meta,
    ):
        fields = AI_ANALYSIS_DETAIL_FIELDS
        read_only_fields = AI_ANALYSIS_READ_ONLY_FIELDS


__all__ = [
    "AIAnalysisCreateSerializer",
    "AIAnalysisDetailSerializer",
    "AIAnalysisListSerializer",
    "AIAnalysisSerializer",
    "AIAnalysisUpdateSerializer",
]

"""
Recommendation serializers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.ai.models import Recommendation
from apps.ai.services import RecommendationService


class RecommendationBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for recommendations.
    """

    class Meta:
        model = Recommendation
        fields: tuple[str, ...] = ()


class RecommendationCreateSerializer(RecommendationBaseSerializer):
    """
    Serializer for creating recommendations.
    """

    class Meta(RecommendationBaseSerializer.Meta):
        fields = (
            "organization",
            "patient",
            "recommendation_type",
            "title",
            "description",
            "confidence_score",
            "source",
            "status",
            "priority",
            "expires_at",
        )

    def create(
        self,
        validated_data: dict[str, object],
    ) -> Recommendation:
        """
        Create a recommendation.
        """

        return RecommendationService.create(
            validated_data=validated_data,
        )


class RecommendationUpdateSerializer(RecommendationBaseSerializer):
    """
    Serializer for updating recommendations.
    """

    class Meta(RecommendationBaseSerializer.Meta):
        fields = (
            "status",
            "priority",
            "confidence_score",
            "source",
            "expires_at",
        )

    def update(
        self,
        instance: Recommendation,
        validated_data: dict[str, object],
    ) -> Recommendation:
        """
        Update a recommendation.
        """

        return RecommendationService.update(
            instance=instance,
            validated_data=validated_data,
        )


class RecommendationDetailSerializer(RecommendationBaseSerializer):
    """
    Serializer for recommendation detail views.
    """

    class Meta(RecommendationBaseSerializer.Meta):
        fields = (
            "id",
            "organization",
            "patient",
            "recommendation_type",
            "title",
            "description",
            "confidence_score",
            "source",
            "status",
            "priority",
            "expires_at",
            "created_at",
            "updated_at",
        )


class RecommendationListSerializer(RecommendationBaseSerializer):
    """
    Serializer for listing recommendations.
    """

    class Meta(RecommendationBaseSerializer.Meta):
        fields = (
            "id",
            "organization",
            "patient",
            "recommendation_type",
            "title",
            "status",
            "priority",
            "confidence_score",
            "created_at",
        )


class RecommendationSerializer(RecommendationBaseSerializer):
    """
    Generic recommendation serializer.
    """

    class Meta(RecommendationBaseSerializer.Meta):
        fields = (
            "id",
            "organization",
            "patient",
            "recommendation_type",
            "title",
            "description",
            "confidence_score",
            "source",
            "status",
            "priority",
            "expires_at",
            "created_at",
            "updated_at",
        )


__all__ = [
    "RecommendationBaseSerializer",
    "RecommendationCreateSerializer",
    "RecommendationDetailSerializer",
    "RecommendationListSerializer",
    "RecommendationSerializer",
    "RecommendationUpdateSerializer",
]

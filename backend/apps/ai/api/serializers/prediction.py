"""
Prediction serializers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.ai.models import Prediction
from apps.ai.services import PredictionService


class PredictionBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for predictions.
    """

    class Meta:
        model = Prediction
        fields: tuple[str, ...] = ()


class PredictionCreateSerializer(PredictionBaseSerializer):
    """
    Serializer for creating predictions.
    """

    class Meta(PredictionBaseSerializer.Meta):
        fields = (
            "organization",
            "patient",
            "ai_model",
            "prediction_type",
            "risk_score",
            "risk_level",
            "input_data",
            "result",
            "explanation",
        )

    def create(
        self,
        validated_data: dict[str, object],
    ) -> Prediction:
        """
        Create a prediction.
        """

        return PredictionService.create(
            validated_data=validated_data,
        )


class PredictionUpdateSerializer(PredictionBaseSerializer):
    """
    Serializer for updating predictions.
    """

    class Meta(PredictionBaseSerializer.Meta):
        fields = (
            "is_reviewed",
            "reviewed_by",
            "reviewed_at",
            "result",
            "explanation",
        )

    def update(
        self,
        instance: Prediction,
        validated_data: dict[str, object],
    ) -> Prediction:
        """
        Update a prediction.
        """

        return PredictionService.update(
            instance=instance,
            validated_data=validated_data,
        )


class PredictionDetailSerializer(PredictionBaseSerializer):
    """
    Serializer for prediction detail views.
    """

    class Meta(PredictionBaseSerializer.Meta):
        fields = (
            "id",
            "organization",
            "patient",
            "ai_model",
            "prediction_type",
            "risk_score",
            "risk_level",
            "input_data",
            "result",
            "explanation",
            "predicted_at",
            "is_reviewed",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        )


class PredictionListSerializer(PredictionBaseSerializer):
    """
    Serializer for listing predictions.
    """

    class Meta(PredictionBaseSerializer.Meta):
        fields = (
            "id",
            "organization",
            "patient",
            "ai_model",
            "prediction_type",
            "risk_score",
            "risk_level",
            "predicted_at",
            "is_reviewed",
        )


class PredictionSerializer(PredictionBaseSerializer):
    """
    Generic prediction serializer.
    """

    class Meta(PredictionBaseSerializer.Meta):
        fields = (
            "id",
            "organization",
            "patient",
            "ai_model",
            "prediction_type",
            "risk_score",
            "risk_level",
            "input_data",
            "result",
            "explanation",
            "predicted_at",
            "is_reviewed",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        )


__all__ = [
    "PredictionBaseSerializer",
    "PredictionCreateSerializer",
    "PredictionDetailSerializer",
    "PredictionListSerializer",
    "PredictionSerializer",
    "PredictionUpdateSerializer",
]

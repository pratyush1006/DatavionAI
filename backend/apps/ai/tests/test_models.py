"""
Tests for AI models.
"""

from __future__ import annotations

from django.db import IntegrityError

from apps.ai.constants import ModelStatus, ModelType
from apps.ai.models import AIModel, Prediction, Recommendation
from apps.common.tests.base import BaseTestCase


class AIModelModelTestCase(BaseTestCase):
    """
    Test cases for the AIModel model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.ai_model = AIModel.objects.create(
            organization=self.organization,
            name="Test Model",
            model_type=ModelType.PREDICTION,
            version="1.0.0",
            status=ModelStatus.READY,
            description="A test AI model",
            accuracy=0.95,
        )

    def test_ai_model_creation(self) -> None:
        """
        AIModel should be created successfully.
        """

        self.assertEqual(
            self.ai_model.organization,
            self.organization,
        )

        self.assertEqual(
            self.ai_model.name,
            "Test Model",
        )

        self.assertEqual(
            self.ai_model.version,
            "1.0.0",
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the model display name.
        """

        self.assertEqual(
            str(self.ai_model),
            "Test Model v1.0.0",
        )

    def test_default_status(self) -> None:
        """
        Default model status should be DRAFT.
        """

        model = AIModel.objects.create(
            organization=self.organization,
            name="Draft Model",
            model_type=ModelType.CLASSIFICATION,
            version="0.1.0",
        )

        self.assertEqual(
            model.status,
            ModelStatus.DRAFT,
        )

    def test_unique_model_per_organization(self) -> None:
        """
        Model name + version should be unique within an organization.
        """

        with self.assertRaises(
            IntegrityError,
        ):
            AIModel.objects.create(
                organization=self.organization,
                name="Test Model",
                model_type=ModelType.PREDICTION,
                version="1.0.0",
            )

    def test_meta_table_name(self) -> None:
        """
        AIModel should use the configured database table.
        """

        self.assertEqual(
            AIModel._meta.db_table,
            "ai_models",
        )

    def test_meta_ordering(self) -> None:
        """
        AIModel should use the configured ordering.
        """

        self.assertEqual(
            AIModel._meta.ordering,
            (
                "name",
                "-version",
            ),
        )


class PredictionModelTestCase(BaseTestCase):
    """
    Test cases for the Prediction model.
    """

    def setUp(self) -> None:
        super().setUp()

        from apps.ai.constants import PredictionType, RiskLevel

        self.prediction = Prediction.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            ai_model=AIModel.objects.create(
                organization=self.organization,
                name="Test Model",
                model_type=ModelType.PREDICTION,
                version="1.0.0",
                status=ModelStatus.READY,
            ),
            prediction_type=PredictionType.SEPSIS_RISK,
            risk_score=0.75,
            risk_level=RiskLevel.HIGH,
            input_data={"age": 65, "temperature": 38.5},
            result={"probability": 0.75, "threshold": 0.5},
            explanation="High sepsis risk due to elevated temperature.",
        )

    def test_prediction_creation(self) -> None:
        """
        Prediction should be created successfully.
        """

        self.assertEqual(
            self.prediction.organization,
            self.organization,
        )

        self.assertEqual(
            self.prediction.risk_score,
            0.75,
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the prediction display string.
        """

        self.assertIn(
            "sepsis_risk",
            str(self.prediction),
        )

    def test_default_is_reviewed(self) -> None:
        """
        is_reviewed should default to False.
        """

        self.assertFalse(
            self.prediction.is_reviewed,
        )

    def test_meta_table_name(self) -> None:
        """
        Prediction should use the configured database table.
        """

        self.assertEqual(
            Prediction._meta.db_table,
            "predictions",
        )

    def test_meta_ordering(self) -> None:
        """
        Prediction should use the configured ordering.
        """

        self.assertEqual(
            Prediction._meta.ordering,
            ("-predicted_at",),
        )


class RecommendationModelTestCase(BaseTestCase):
    """
    Test cases for the Recommendation model.
    """

    def setUp(self) -> None:
        super().setUp()

        from apps.ai.constants import (
            RecommendationPriority,
            RecommendationStatus,
            RecommendationType,
        )

        self.recommendation = Recommendation.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            recommendation_type=RecommendationType.TREATMENT,
            title="Start Antibiotics",
            description="Initiate broad-spectrum antibiotics immediately.",
            confidence_score=0.9,
            source="AI Model v1.0",
            status=RecommendationStatus.PENDING,
            priority=RecommendationPriority.HIGH,
        )

    def test_recommendation_creation(self) -> None:
        """
        Recommendation should be created successfully.
        """

        self.assertEqual(
            self.recommendation.organization,
            self.organization,
        )

        self.assertEqual(
            self.recommendation.title,
            "Start Antibiotics",
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the recommendation display string.
        """

        self.assertIn(
            "Start Antibiotics",
            str(self.recommendation),
        )

    def test_default_status(self) -> None:
        """
        Default recommendation status should be PENDING.
        """

        from apps.ai.constants import RecommendationStatus

        rec = Recommendation.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            recommendation_type="treatment",
            title="Test",
            description="Test description",
        )

        self.assertEqual(
            rec.status,
            RecommendationStatus.PENDING,
        )

    def test_default_priority(self) -> None:
        """
        Default recommendation priority should be MEDIUM.
        """

        from apps.ai.constants import RecommendationPriority

        rec = Recommendation.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            recommendation_type="treatment",
            title="Test",
            description="Test description",
        )

        self.assertEqual(
            rec.priority,
            RecommendationPriority.MEDIUM,
        )

    def test_meta_table_name(self) -> None:
        """
        Recommendation should use the configured database table.
        """

        self.assertEqual(
            Recommendation._meta.db_table,
            "recommendations",
        )

    def test_meta_ordering(self) -> None:
        """
        Recommendation should use the configured ordering.
        """

        self.assertEqual(
            Recommendation._meta.ordering,
            ("-created_at",),
        )


__all__ = [
    "AIModelModelTestCase",
    "PredictionModelTestCase",
    "RecommendationModelTestCase",
]

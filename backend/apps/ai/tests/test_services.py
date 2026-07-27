"""
Tests for AI services.
"""

from __future__ import annotations

from apps.ai.constants import (
    ModelStatus,
    ModelType,
    PredictionType,
    RecommendationPriority,
    RecommendationStatus,
    RecommendationType,
    RiskLevel,
)
from apps.ai.models import Prediction, Recommendation
from apps.ai.services import (
    PredictionService,
    RecommendationService,
)
from apps.ai.tests.factories import (
    AIModelFactory,
    PatientFactory,
    PredictionFactory,
    RecommendationFactory,
)
from apps.common.tests.base import BaseTestCase


class PredictionServiceTestCase(BaseTestCase):
    """
    Test cases for PredictionService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.ai_model = AIModelFactory(
            organization=self.organization,
            name="Test Model",
            model_type=ModelType.PREDICTION,
            version="1.0.0",
            status=ModelStatus.READY,
        )

        self.patient = PatientFactory(
            organization=self.organization,
        )

    def test_create_prediction(self) -> None:
        """
        Prediction should be created successfully.
        """

        prediction = PredictionService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "ai_model": self.ai_model,
                "prediction_type": PredictionType.SEPSIS_RISK,
                "risk_score": 0.75,
                "risk_level": RiskLevel.HIGH,
                "input_data": {"age": 65},
                "result": {"probability": 0.75},
            },
        )

        self.assertIsInstance(
            prediction,
            Prediction,
        )

        self.assertEqual(
            prediction.risk_score,
            0.75,
        )

    def test_create_prediction_persists_to_database(self) -> None:
        """
        Created prediction should be persisted.
        """

        initial_count = Prediction.objects.count()

        PredictionService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "ai_model": self.ai_model,
                "prediction_type": PredictionType.FALL_RISK,
                "risk_score": 0.3,
                "risk_level": RiskLevel.LOW,
                "input_data": {},
                "result": {},
            },
        )

        self.assertEqual(
            Prediction.objects.count(),
            initial_count + 1,
        )

    def test_update_prediction(self) -> None:
        """
        Prediction should be updated successfully.
        """

        prediction = PredictionFactory(
            organization=self.organization,
            patient=self.patient,
            ai_model=self.ai_model,
            prediction_type=PredictionType.READMISSION_RISK,
            risk_score=0.5,
            risk_level=RiskLevel.MEDIUM,
        )

        updated_prediction = PredictionService.update(
            instance=prediction,
            validated_data={
                "is_reviewed": True,
                "result": {"probability": 0.8},
            },
        )

        updated_prediction.refresh_from_db()

        self.assertTrue(
            updated_prediction.is_reviewed,
        )

    def test_delete_prediction(self) -> None:
        """
        Prediction should be deleted successfully.
        """

        prediction = PredictionFactory(
            organization=self.organization,
            patient=self.patient,
            ai_model=self.ai_model,
            prediction_type=PredictionType.DISEASE_PROGRESSION,
            risk_score=0.4,
            risk_level=RiskLevel.MEDIUM,
        )

        prediction_id = prediction.pk

        PredictionService.delete(
            instance=prediction,
        )

        self.assertFalse(
            Prediction.objects.filter(
                pk=prediction_id,
            ).exists(),
        )

    def test_bulk_create_predictions(self) -> None:
        """
        Multiple predictions should be created successfully.
        """

        predictions = PredictionService.bulk_create(
            validated_data_list=[
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "ai_model": self.ai_model,
                    "prediction_type": PredictionType.SEPSIS_RISK,
                    "risk_score": 0.7,
                    "risk_level": RiskLevel.HIGH,
                    "input_data": {},
                    "result": {},
                },
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "ai_model": self.ai_model,
                    "prediction_type": PredictionType.FALL_RISK,
                    "risk_score": 0.2,
                    "risk_level": RiskLevel.LOW,
                    "input_data": {},
                    "result": {},
                },
            ],
        )

        self.assertEqual(
            len(predictions),
            2,
        )


class RecommendationServiceTestCase(BaseTestCase):
    """
    Test cases for RecommendationService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = PatientFactory(
            organization=self.organization,
        )

    def test_create_recommendation(self) -> None:
        """
        Recommendation should be created successfully.
        """

        recommendation = RecommendationService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "recommendation_type": RecommendationType.TREATMENT,
                "title": "Start Antibiotics",
                "description": "Initiate broad-spectrum antibiotics immediately.",
                "confidence_score": 0.9,
                "source": "AI Model v1.0",
                "status": RecommendationStatus.PENDING,
                "priority": RecommendationPriority.HIGH,
            },
        )

        self.assertIsInstance(
            recommendation,
            Recommendation,
        )

        self.assertEqual(
            recommendation.title,
            "Start Antibiotics",
        )

    def test_create_recommendation_persists_to_database(self) -> None:
        """
        Created recommendation should be persisted.
        """

        initial_count = Recommendation.objects.count()

        RecommendationService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "recommendation_type": RecommendationType.FOLLOW_UP,
                "title": "Follow-up Visit",
                "description": "Schedule follow-up in 2 weeks.",
            },
        )

        self.assertEqual(
            Recommendation.objects.count(),
            initial_count + 1,
        )

    def test_update_recommendation(self) -> None:
        """
        Recommendation should be updated successfully.
        """

        recommendation = RecommendationFactory(
            organization=self.organization,
            patient=self.patient,
            recommendation_type=RecommendationType.TREATMENT,
            title="Original Title",
            status=RecommendationStatus.PENDING,
            priority=RecommendationPriority.MEDIUM,
        )

        updated_recommendation = RecommendationService.update(
            instance=recommendation,
            validated_data={
                "status": RecommendationStatus.ACCEPTED,
                "priority": RecommendationPriority.HIGH,
            },
        )

        updated_recommendation.refresh_from_db()

        self.assertEqual(
            updated_recommendation.status,
            RecommendationStatus.ACCEPTED,
        )

    def test_delete_recommendation(self) -> None:
        """
        Recommendation should be deleted successfully.
        """

        recommendation = RecommendationFactory(
            organization=self.organization,
            patient=self.patient,
            recommendation_type=RecommendationType.PREVENTIVE_CARE,
            title="Vaccination",
            status=RecommendationStatus.PENDING,
            priority=RecommendationPriority.MEDIUM,
        )

        recommendation_id = recommendation.pk

        RecommendationService.delete(
            instance=recommendation,
        )

        self.assertFalse(
            Recommendation.objects.filter(
                pk=recommendation_id,
            ).exists(),
        )

    def test_bulk_create_recommendations(self) -> None:
        """
        Multiple recommendations should be created successfully.
        """

        recommendations = RecommendationService.bulk_create(
            validated_data_list=[
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "recommendation_type": RecommendationType.TREATMENT,
                    "title": "Treatment Plan A",
                    "description": "Description A",
                },
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "recommendation_type": RecommendationType.LIFESTYLE,
                    "title": "Lifestyle Change",
                    "description": "Description B",
                },
            ],
        )

        self.assertEqual(
            len(recommendations),
            2,
        )


__all__ = [
    "PredictionServiceTestCase",
    "RecommendationServiceTestCase",
]

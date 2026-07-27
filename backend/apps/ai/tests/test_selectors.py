"""
Tests for AI selectors.
"""

from __future__ import annotations

from apps.ai.constants import (
    ModelStatus,
    ModelType,
    PredictionType,
    RecommendationStatus,
    RecommendationType,
    RiskLevel,
)
from apps.ai.selectors import (
    PredictionSelector,
    RecommendationSelector,
)
from apps.ai.tests.factories import (
    AIModelFactory,
    PatientFactory,
    PredictionFactory,
    RecommendationFactory,
)
from apps.common.tests.base import BaseTestCase


class PredictionSelectorTestCase(BaseTestCase):
    """
    Test cases for PredictionSelector.
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

        self.prediction = PredictionFactory(
            organization=self.organization,
            patient=PatientFactory(organization=self.organization),
            ai_model=self.ai_model,
            prediction_type=PredictionType.SEPSIS_RISK,
            risk_score=0.75,
            risk_level=RiskLevel.HIGH,
        )

    def test_queryset(self) -> None:
        """
        queryset() should return a queryset.
        """

        queryset = PredictionSelector.queryset()

        self.assertIn(
            self.prediction,
            queryset,
        )

    def test_list(self) -> None:
        """
        list() should return all predictions.
        """

        predictions = PredictionSelector.list()

        self.assertEqual(
            predictions.count(),
            1,
        )

    def test_get(self) -> None:
        """
        get() should return the requested prediction.
        """

        prediction = PredictionSelector.get(
            prediction_id=self.prediction.id,
        )

        self.assertEqual(
            prediction,
            self.prediction,
        )

    def test_list_by_patient(self) -> None:
        """
        list_by_patient() should filter by patient.
        """

        predictions = PredictionSelector.list_by_patient(
            patient_id=self.prediction.patient_id,
        )

        self.assertEqual(
            predictions.count(),
            1,
        )

    def test_list_by_model(self) -> None:
        """
        list_by_model() should filter by model.
        """

        predictions = PredictionSelector.list_by_model(
            ai_model_id=self.ai_model.id,
        )

        self.assertEqual(
            predictions.count(),
            1,
        )

    def test_list_by_organization(self) -> None:
        """
        list_by_organization() should filter by organization.
        """

        predictions = PredictionSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertEqual(
            predictions.count(),
            1,
        )

    def test_search(self) -> None:
        """
        search() should find matching predictions.
        """

        predictions = PredictionSelector.search(
            organization=self.organization,
            query="sepsis",
        )

        self.assertEqual(
            predictions.count(),
            1,
        )

        self.assertEqual(
            predictions.first(),
            self.prediction,
        )

    def test_count(self) -> None:
        """
        count() should return the prediction count.
        """

        self.assertEqual(
            PredictionSelector.count(
                organization=self.organization,
            ),
            1,
        )


class RecommendationSelectorTestCase(BaseTestCase):
    """
    Test cases for RecommendationSelector.
    """

    def setUp(self) -> None:
        super().setUp()

        self.recommendation = RecommendationFactory(
            organization=self.organization,
            patient=PatientFactory(organization=self.organization),
            recommendation_type=RecommendationType.TREATMENT,
            title="Start Antibiotics",
            status=RecommendationStatus.PENDING,
            priority="medium",
        )

    def test_queryset(self) -> None:
        """
        queryset() should return a queryset.
        """

        queryset = RecommendationSelector.queryset()

        self.assertIn(
            self.recommendation,
            queryset,
        )

    def test_list(self) -> None:
        """
        list() should return all recommendations.
        """

        recommendations = RecommendationSelector.list()

        self.assertEqual(
            recommendations.count(),
            1,
        )

    def test_get(self) -> None:
        """
        get() should return the requested recommendation.
        """

        recommendation = RecommendationSelector.get(
            recommendation_id=self.recommendation.id,
        )

        self.assertEqual(
            recommendation,
            self.recommendation,
        )

    def test_list_by_patient(self) -> None:
        """
        list_by_patient() should filter by patient.
        """

        recommendations = RecommendationSelector.list_by_patient(
            patient_id=self.recommendation.patient_id,
        )

        self.assertEqual(
            recommendations.count(),
            1,
        )

    def test_list_by_organization(self) -> None:
        """
        list_by_organization() should filter by organization.
        """

        recommendations = RecommendationSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertEqual(
            recommendations.count(),
            1,
        )

    def test_list_active(self) -> None:
        """
        list_active() should return active recommendations.
        """

        recommendations = RecommendationSelector.list_active(
            organization=self.organization,
        )

        self.assertEqual(
            recommendations.count(),
            1,
        )

        self.assertEqual(
            recommendations.first(),
            self.recommendation,
        )

    def test_search(self) -> None:
        """
        search() should find matching recommendations.
        """

        recommendations = RecommendationSelector.search(
            organization=self.organization,
            query="antibiotics",
        )

        self.assertEqual(
            recommendations.count(),
            1,
        )

        self.assertEqual(
            recommendations.first(),
            self.recommendation,
        )

    def test_count(self) -> None:
        """
        count() should return the recommendation count.
        """

        self.assertEqual(
            RecommendationSelector.count(
                organization=self.organization,
            ),
            1,
        )


__all__ = [
    "PredictionSelectorTestCase",
    "RecommendationSelectorTestCase",
]

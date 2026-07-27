"""
Factories for AI tests.
"""

from __future__ import annotations

from datetime import date

import factory

from apps.ai.constants import (
    ModelStatus,
    ModelType,
    PredictionType,
    RecommendationPriority,
    RecommendationStatus,
    RecommendationType,
    RiskLevel,
)
from apps.ai.models import AIModel, Prediction, Recommendation
from apps.platform.organizations.tests.factories import OrganizationFactory


class AIModelFactory(factory.django.DjangoModelFactory):
    """
    Factory for AIModel model.
    """

    class Meta:
        model = AIModel

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    name = factory.Sequence(
        lambda n: f"AI Model {n}",
    )

    model_type = ModelType.PREDICTION

    version = factory.Sequence(
        lambda n: f"1.{n}.0",
    )

    status = ModelStatus.READY

    description = "A test AI model"

    accuracy = 0.95

    metadata = {}


class PatientFactory(factory.django.DjangoModelFactory):
    """
    Factory for Patient model.
    """

    class Meta:
        model = "patients.Patient"

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    mrn = factory.Sequence(
        lambda n: f"MRN{n:06d}",
    )

    first_name = factory.Faker(
        "first_name",
    )

    middle_name = ""

    last_name = factory.Faker(
        "last_name",
    )

    preferred_name = ""

    date_of_birth = factory.LazyFunction(
        lambda: date(1995, 5, 20),
    )

    gender = "male"

    marital_status = ""

    blood_group = ""

    phone = ""

    email = ""

    address = ""

    city = ""

    state = ""

    country = "India"

    postal_code = ""

    status = "active"


class PredictionFactory(factory.django.DjangoModelFactory):
    """
    Factory for Prediction model.
    """

    class Meta:
        model = Prediction

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
    )

    ai_model = factory.SubFactory(
        AIModelFactory,
    )

    prediction_type = PredictionType.SEPSIS_RISK

    risk_score = 0.75

    risk_level = RiskLevel.HIGH

    input_data = {"age": 65, "temperature": 38.5}

    result = {"probability": 0.75, "threshold": 0.5}

    explanation = "High sepsis risk due to elevated temperature."

    is_reviewed = False


class RecommendationFactory(factory.django.DjangoModelFactory):
    """
    Factory for Recommendation model.
    """

    class Meta:
        model = Recommendation

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
    )

    recommendation_type = RecommendationType.TREATMENT

    title = factory.Faker(
        "sentence",
        nb_words=4,
    )

    description = factory.Faker(
        "text",
    )

    confidence_score = 0.9

    source = "AI Model v1.0"

    status = RecommendationStatus.PENDING

    priority = RecommendationPriority.MEDIUM

    expires_at = None


__all__ = [
    "AIModelFactory",
    "PatientFactory",
    "PredictionFactory",
    "RecommendationFactory",
]

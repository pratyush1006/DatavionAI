"""
AI-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class ModelType(models.TextChoices):
    """
    Supported AI model types.
    """

    PREDICTION = "prediction", "Prediction"
    CLASSIFICATION = "classification", "Classification"
    NLP = "nlp", "NLP"
    IMAGE_ANALYSIS = "image_analysis", "Image Analysis"
    RECOMMENDATION = "recommendation", "Recommendation"


class ModelStatus(models.TextChoices):
    """
    AI model lifecycle status.
    """

    DRAFT = "draft", "Draft"
    TRAINING = "training", "Training"
    READY = "ready", "Ready"
    DEPLOYED = "deployed", "Deployed"
    RETIRED = "retired", "Retired"


class PredictionType(models.TextChoices):
    """
    Supported prediction types.
    """

    READMISSION_RISK = "readmission_risk", "Readmission Risk"
    DISEASE_PROGRESSION = "disease_progression", "Disease Progression"
    SEPSIS_RISK = "sepsis_risk", "Sepsis Risk"
    FALL_RISK = "fall_risk", "Fall Risk"
    MEDICATION_ADHERENCE = "medication_adherence", "Medication Adherence"
    COMPLICATION_RISK = "complication_risk", "Complication Risk"


class RiskLevel(models.TextChoices):
    """
    Clinical risk levels.
    """

    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class RecommendationType(models.TextChoices):
    """
    Supported recommendation types.
    """

    TREATMENT = "treatment", "Treatment"
    FOLLOW_UP = "follow_up", "Follow Up"
    PREVENTIVE_CARE = "preventive_care", "Preventive Care"
    LIFESTYLE = "lifestyle", "Lifestyle"
    MEDICATION = "medication", "Medication"
    REFERRAL = "referral", "Referral"


class RecommendationStatus(models.TextChoices):
    """
    Recommendation lifecycle status.
    """

    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
    EXPIRED = "expired", "Expired"


class RecommendationPriority(models.TextChoices):
    """
    Recommendation priority levels.
    """

    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"


DEFAULT_MODEL_STATUS: Final[str] = ModelStatus.DRAFT


__all__ = [
    "DEFAULT_MODEL_STATUS",
    "ModelStatus",
    "ModelType",
    "PredictionType",
    "RecommendationPriority",
    "RecommendationStatus",
    "RecommendationType",
    "RiskLevel",
]

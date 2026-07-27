"""
AI service exports.
"""

from __future__ import annotations

from apps.ai.services.prediction import (
    PredictionService,
    create_prediction,
    delete_prediction,
    update_prediction,
)
from apps.ai.services.recommendation import (
    RecommendationService,
    create_recommendation,
    delete_recommendation,
    update_recommendation,
)

__all__ = [
    "PredictionService",
    "RecommendationService",
    "create_prediction",
    "create_recommendation",
    "delete_prediction",
    "delete_recommendation",
    "update_prediction",
    "update_recommendation",
]

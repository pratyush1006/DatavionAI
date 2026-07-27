"""
AI selector exports.
"""

from __future__ import annotations

from apps.ai.selectors.prediction import PredictionSelector
from apps.ai.selectors.recommendation import RecommendationSelector

__all__ = [
    "PredictionSelector",
    "RecommendationSelector",
]

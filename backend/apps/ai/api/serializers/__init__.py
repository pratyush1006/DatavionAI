"""
AI serializer exports.
"""

from __future__ import annotations

from .prediction import (
    PredictionBaseSerializer,
    PredictionCreateSerializer,
    PredictionDetailSerializer,
    PredictionListSerializer,
    PredictionSerializer,
    PredictionUpdateSerializer,
)
from .recommendation import (
    RecommendationBaseSerializer,
    RecommendationCreateSerializer,
    RecommendationDetailSerializer,
    RecommendationListSerializer,
    RecommendationSerializer,
    RecommendationUpdateSerializer,
)

__all__ = [
    "PredictionBaseSerializer",
    "PredictionCreateSerializer",
    "PredictionDetailSerializer",
    "PredictionListSerializer",
    "PredictionSerializer",
    "PredictionUpdateSerializer",
    "RecommendationBaseSerializer",
    "RecommendationCreateSerializer",
    "RecommendationDetailSerializer",
    "RecommendationListSerializer",
    "RecommendationSerializer",
    "RecommendationUpdateSerializer",
]

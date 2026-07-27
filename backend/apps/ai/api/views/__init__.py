"""
AI API view exports.
"""

from __future__ import annotations

from .bulk import (
    PredictionBulkCreateAPIView,
    RecommendationBulkCreateAPIView,
)
from .prediction import (
    PredictionListCreateAPIView,
    PredictionRetrieveUpdateDestroyAPIView,
)
from .recommendation import (
    RecommendationListCreateAPIView,
    RecommendationRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "PredictionBulkCreateAPIView",
    "PredictionListCreateAPIView",
    "PredictionRetrieveUpdateDestroyAPIView",
    "RecommendationBulkCreateAPIView",
    "RecommendationListCreateAPIView",
    "RecommendationRetrieveUpdateDestroyAPIView",
]

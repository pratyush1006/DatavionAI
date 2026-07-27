"""
AI API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.ai.api.views import (
    PredictionBulkCreateAPIView,
    PredictionListCreateAPIView,
    PredictionRetrieveUpdateDestroyAPIView,
    RecommendationBulkCreateAPIView,
    RecommendationListCreateAPIView,
    RecommendationRetrieveUpdateDestroyAPIView,
)

app_name = "ai"

urlpatterns = [
    path(
        "predictions/",
        PredictionListCreateAPIView.as_view(),
        name="prediction-list-create",
    ),
    path(
        "predictions/<uuid:prediction_id>/",
        PredictionRetrieveUpdateDestroyAPIView.as_view(),
        name="prediction-detail",
    ),
    path(
        "predictions/bulk/",
        PredictionBulkCreateAPIView.as_view(),
        name="prediction-bulk-create",
    ),
    path(
        "recommendations/",
        RecommendationListCreateAPIView.as_view(),
        name="recommendation-list-create",
    ),
    path(
        "recommendations/<uuid:recommendation_id>/",
        RecommendationRetrieveUpdateDestroyAPIView.as_view(),
        name="recommendation-detail",
    ),
    path(
        "recommendations/bulk/",
        RecommendationBulkCreateAPIView.as_view(),
        name="recommendation-bulk-create",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

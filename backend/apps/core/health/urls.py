"""
URL configuration for the Core Health module.
"""

from __future__ import annotations

from django.urls import path

from .views import (
    HealthAPIView,
    LivenessAPIView,
    ReadinessAPIView,
)

app_name = "health"

urlpatterns = [
    path(
        "",
        HealthAPIView.as_view(),
        name="health",
    ),
    path(
        "live/",
        LivenessAPIView.as_view(),
        name="liveness",
    ),
    path(
        "ready/",
        ReadinessAPIView.as_view(),
        name="readiness",
    ),
]


__all__ = [
    "app_name",
    "urlpatterns",
]

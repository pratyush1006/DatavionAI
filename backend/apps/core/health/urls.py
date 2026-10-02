"""
URL configuration for the Datavion AI Core Health module.

This module exposes infrastructure health endpoints used by:

- Kubernetes
- Docker
- Load Balancers
- API Gateways
- Cloud Platforms
- Monitoring Systems

Available endpoints:

    GET /health/
        Overall application health.

    GET /health/live/
        Liveness probe.

    GET /health/ready/
        Readiness probe.
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
    # ------------------------------------------------------------------
    # Overall Health
    # ------------------------------------------------------------------
    path(
        "",
        HealthAPIView.as_view(),
        name="health",
    ),
    # ------------------------------------------------------------------
    # Kubernetes / Docker Liveness Probe
    # ------------------------------------------------------------------
    path(
        "live/",
        LivenessAPIView.as_view(),
        name="liveness",
    ),
    # ------------------------------------------------------------------
    # Kubernetes / Docker Readiness Probe
    # ------------------------------------------------------------------
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

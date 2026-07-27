"""
URL configuration for the DatavionOS Core application.

The Core application exposes infrastructure endpoints shared
across the platform.

Current infrastructure routes:

- Health checks
- Liveness probe
- Readiness probe

Additional platform-level endpoints can be added here without
affecting business modules.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "core"


urlpatterns = [
    # ------------------------------------------------------------------
    # Infrastructure Health
    # ------------------------------------------------------------------
    path(
        "health/",
        include(
            "apps.core.health.urls",
            namespace="health",
        ),
    ),
]


__all__ = [
    "app_name",
    "urlpatterns",
]

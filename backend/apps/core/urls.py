"""
URL configuration for the Core application.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

app_name = "core"

urlpatterns = [
    path(
        "health/",
        include(
            (
                "apps.core.health.urls",
                "health",
            ),
            namespace="health",
        ),
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

"""
URL configuration for the Core application.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "core"

urlpatterns = [
    path(
        "health/",
        include(
            "apps.core.health.urls",
            namespace="health",
        ),
    ),
]

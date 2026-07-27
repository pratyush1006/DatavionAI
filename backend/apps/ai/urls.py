"""
AI API URL patterns.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "ai"

urlpatterns = [
    path(
        "",
        include("apps.ai.api.urls"),
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

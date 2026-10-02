"""
URL configuration for the Audit application.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

app_name = "audit"

urlpatterns = [
    path(
        "",
        include(
            "apps.platform.audit.api.urls",
        ),
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

"""
URL configuration for the Audit application.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include(
            "apps.audit.api.urls",
        ),
    ),
]

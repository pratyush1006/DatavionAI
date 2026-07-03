"""
URL configuration for the Storage application.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include(
            "apps.storage.api.urls",
        ),
    ),
]

"""
Geography URL configuration.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include(
            "apps.platform.geography.api.urls",
        ),
    ),
]


app_name = "geography"

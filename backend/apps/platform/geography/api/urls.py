"""
Geography API router.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "geography-api"


urlpatterns = [
    path(
        "",
        include(
            (
                "apps.platform.geography.api.geography.urls",
                "geography",
            ),
        ),
    ),
]


__all__: list[str] = [
    "app_name",
    "urlpatterns",
]

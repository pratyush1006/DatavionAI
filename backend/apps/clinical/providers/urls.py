"""
Provider URL configuration.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

urlpatterns = [
    path(
        "",
        include(
            "apps.clinical.providers.api.urls",
        ),
    ),
]


__all__ = ("urlpatterns",)

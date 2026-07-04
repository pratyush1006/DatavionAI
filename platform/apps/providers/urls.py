"""
Provider URL configuration.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "providers"

urlpatterns = [
    path(
        "",
        include("apps.providers.api.urls"),
    ),
]

__all__ = [
    "urlpatterns",
]

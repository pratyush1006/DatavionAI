"""
URL configuration for the Configuration application.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.configuration.api.urls"),
    ),
]

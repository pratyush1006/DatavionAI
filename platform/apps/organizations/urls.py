"""
Organization URL configuration.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "organizations"

urlpatterns = [
    path(
        "",
        include("apps.organizations.api.urls"),
    ),
]

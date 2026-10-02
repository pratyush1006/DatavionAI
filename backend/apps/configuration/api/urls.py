"""
API URL configuration for the Configuration application.
"""

from __future__ import annotations

from django.urls import path

from apps.configuration.api.views import (
    ConfigurationListCreateAPIView,
    ConfigurationRetrieveUpdateDestroyAPIView,
)

app_name = "configuration-api"

urlpatterns = [
    path(
        "",
        ConfigurationListCreateAPIView.as_view(),
        name="configuration-list-create",
    ),
    path(
        "<str:key>/",
        ConfigurationRetrieveUpdateDestroyAPIView.as_view(),
        name="configuration-detail",
    ),
]

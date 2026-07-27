"""
Provider API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.clinical.providers.api.views import (
    ProviderListCreateAPIView,
    ProviderRetrieveUpdateDestroyAPIView,
)

app_name = "providers-api"

urlpatterns = [
    path(
        "",
        ProviderListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:provider_id>/",
        ProviderRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

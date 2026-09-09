"""
Provider API routes.

Includes:

- Provider CRUD endpoints
"""

from __future__ import annotations

from django.urls import path

from apps.clinical.providers.api.views import (
    ProviderListCreateAPIView,
    ProviderRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # ========================================================
    # CRUD
    # ========================================================
    path(
        "",
        ProviderListCreateAPIView.as_view(),
        name="provider-list-create",
    ),
    path(
        "<uuid:provider_id>/",
        ProviderRetrieveUpdateDestroyAPIView.as_view(),
        name="provider-detail",
    ),
]


__all__ = ("urlpatterns",)

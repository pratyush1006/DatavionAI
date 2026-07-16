"""
API URL configuration for the Storage application.
"""

from __future__ import annotations

from django.urls import path

from apps.storage.api.views import (
    AssetListCreateAPIView,
    AssetRetrieveUpdateDestroyAPIView,
)

app_name = "storage-api"

urlpatterns = [
    path(
        "",
        AssetListCreateAPIView.as_view(),
        name="asset-list-create",
    ),
    path(
        "<uuid:pk>/",
        AssetRetrieveUpdateDestroyAPIView.as_view(),
        name="asset-detail",
    ),
]

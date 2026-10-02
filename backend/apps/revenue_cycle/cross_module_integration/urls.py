"""URL routes for Revenue Cycle cross-module integration."""

from __future__ import annotations

from django.urls import path

from .api.views import (
    RevenueCycleIntegrationIngestAPIView,
    RevenueCycleIntegrationListAPIView,
    RevenueCycleIntegrationProcessAPIView,
)

app_name = "revenue_cycle_cross_module_integration"

urlpatterns = [
    path(
        "records/",
        RevenueCycleIntegrationListAPIView.as_view(),
        name="record-list",
    ),
    path(
        "records/ingest/",
        RevenueCycleIntegrationIngestAPIView.as_view(),
        name="record-ingest",
    ),
    path(
        "records/<uuid:record_id>/process/",
        RevenueCycleIntegrationProcessAPIView.as_view(),
        name="record-process",
    ),
]

__all__ = ("app_name", "urlpatterns")

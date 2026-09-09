"""URL routes for Revenue Analytics."""

from __future__ import annotations

from django.urls import path

from .api.views import RevenueAnalyticsGenerateAPIView, RevenueAnalyticsListAPIView

app_name = "revenue_cycle_revenue_analytics"

urlpatterns = [
    path(
        "snapshots/",
        RevenueAnalyticsListAPIView.as_view(),
        name="snapshot-list",
    ),
    path(
        "snapshots/generate/",
        RevenueAnalyticsGenerateAPIView.as_view(),
        name="snapshot-generate",
    ),
]

__all__ = ("app_name", "urlpatterns")

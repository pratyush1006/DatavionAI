"""URL routes for Revenue Analytics."""

from __future__ import annotations

from django.urls import path

from .api.views import (
    FinanceManagerDashboardAPIView,
    RevenueAnalyticsGenerateAPIView,
    RevenueAnalyticsListAPIView,
)

app_name = "revenue_cycle_revenue_analytics"

urlpatterns = [
    path(
        "dashboard/",
        FinanceManagerDashboardAPIView.as_view(),
        name="finance-manager-dashboard",
    ),
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

"""
URL patterns for the RCM Metric module.
"""

from __future__ import annotations

from apps.revenue_cycle.analytics.api.views import (
    RcmMetricListCreateAPIView,
    RcmMetricRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "rcm_metrics"

urlpatterns = [
    path(
        "",
        RcmMetricListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:metric_id>/",
        RcmMetricRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

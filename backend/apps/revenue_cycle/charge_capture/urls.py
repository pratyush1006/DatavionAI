"""
URL patterns for the Charge Capture module.
"""

from __future__ import annotations

from apps.revenue_cycle.charge_capture.api.views import (
    ChargeCaptureListCreateAPIView,
    ChargeCaptureRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "charge_captures"

urlpatterns = [
    path(
        "",
        ChargeCaptureListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:charge_id>/",
        ChargeCaptureRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

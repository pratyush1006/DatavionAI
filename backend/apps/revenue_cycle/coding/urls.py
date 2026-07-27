"""
URL patterns for the Coding Entry module.
"""

from __future__ import annotations

from apps.revenue_cycle.coding.api.views import (
    ChargeCodingListCreateAPIView,
    ChargeCodingRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "coding_entries"

urlpatterns = [
    path(
        "",
        ChargeCodingListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:coding_id>/",
        ChargeCodingRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

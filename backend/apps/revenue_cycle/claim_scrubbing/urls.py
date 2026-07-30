"""
URL patterns for the Scrub Result module.
"""

from __future__ import annotations

from apps.revenue_cycle.claim_scrubbing.api.views import (
    ClaimScrubResultListCreateAPIView,
    ClaimScrubResultRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "scrub_results"

urlpatterns = [
    path(
        "",
        ClaimScrubResultListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:scrub_id>/",
        ClaimScrubResultRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

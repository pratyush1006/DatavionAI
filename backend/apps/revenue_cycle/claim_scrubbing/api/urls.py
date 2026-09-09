"""URL routes for claim scrubbing APIs."""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.claim_scrubbing.api.views import (
    ClaimScrubDetailAPIView,
    ClaimScrubListCreateAPIView,
    ClaimScrubOverrideAPIView,
    ClaimScrubRunAPIView,
)

urlpatterns = [
    path(
        "scrubs/", ClaimScrubListCreateAPIView.as_view(), name="claim-scrub-list-create"
    ),
    path(
        "scrubs/<uuid:scrub_id>/",
        ClaimScrubDetailAPIView.as_view(),
        name="claim-scrub-detail",
    ),
    path(
        "scrubs/<uuid:scrub_id>/run/",
        ClaimScrubRunAPIView.as_view(),
        name="claim-scrub-run",
    ),
    path(
        "scrubs/<uuid:scrub_id>/override/",
        ClaimScrubOverrideAPIView.as_view(),
        name="claim-scrub-override",
    ),
]

__all__ = ("urlpatterns",)

"""
URL patterns for the Claim Appeal module.
"""

from __future__ import annotations

from apps.revenue_cycle.appeals.api.views import (
    ClaimAppealListCreateAPIView,
    ClaimAppealRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "claim_appeals"

urlpatterns = [
    path(
        "",
        ClaimAppealListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:appeal_id>/",
        ClaimAppealRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

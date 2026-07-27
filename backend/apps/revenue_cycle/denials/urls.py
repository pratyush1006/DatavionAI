"""
URL patterns for the Claim Denial module.
"""

from __future__ import annotations

from apps.revenue_cycle.denials.api.views import (
    ClaimDenialListCreateAPIView,
    ClaimDenialRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "claim_denials"

urlpatterns = [
    path(
        "",
        ClaimDenialListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:denial_id>/",
        ClaimDenialRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

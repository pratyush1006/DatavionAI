"""
URL patterns for the Claim Submission module.
"""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.claim_submission.api.views import (
    ClaimSubmissionListCreateAPIView,
    ClaimSubmissionRetrieveUpdateDestroyAPIView,
)

app_name = "claim_submissions"

urlpatterns = [
    path(
        "",
        ClaimSubmissionListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:submission_id>/",
        ClaimSubmissionRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

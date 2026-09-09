"""URL routes for claim submission APIs."""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.claim_submission.api.views import (
    ClaimSubmissionDetailAPIView,
    ClaimSubmissionListCreateAPIView,
    ClaimSubmissionRestoreAPIView,
    ClaimSubmissionTransitionAPIView,
)

urlpatterns = [
    path(
        "submissions/",
        ClaimSubmissionListCreateAPIView.as_view(),
        name="claim-submission-list-create",
    ),
    path(
        "submissions/<uuid:submission_id>/",
        ClaimSubmissionDetailAPIView.as_view(),
        name="claim-submission-detail",
    ),
    path(
        "submissions/<uuid:submission_id>/transition/",
        ClaimSubmissionTransitionAPIView.as_view(),
        name="claim-submission-transition",
    ),
    path(
        "submissions/<uuid:submission_id>/restore/",
        ClaimSubmissionRestoreAPIView.as_view(),
        name="claim-submission-restore",
    ),
]

__all__ = ("urlpatterns",)

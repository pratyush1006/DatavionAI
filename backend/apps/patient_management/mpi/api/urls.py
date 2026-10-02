"""
Master Patient Index API routes.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.mpi.api.views import (
    MPICandidateListAPIView,
    MPICandidateReviewAPIView,
    MPIDetailAPIView,
    MPILifecycleAPIView,
    MPIListCreateAPIView,
    MPIMergeAPIView,
    MPIRestoreAPIView,
    MPIReverseMergeAPIView,
)

app_name = "patient_mpi"

urlpatterns = [
    path(
        "",
        MPIListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:record_id>/",
        MPIDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:record_id>/lifecycle/",
        MPILifecycleAPIView.as_view(),
        name="lifecycle",
    ),
    path(
        "<uuid:record_id>/restore/",
        MPIRestoreAPIView.as_view(),
        name="restore",
    ),
    path(
        "matches/",
        MPICandidateListAPIView.as_view(),
        name="matches",
    ),
    path(
        "matches/<uuid:candidate_id>/review/",
        MPICandidateReviewAPIView.as_view(),
        name="match-review",
    ),
    path(
        "merge/",
        MPIMergeAPIView.as_view(),
        name="merge",
    ),
    path(
        "<uuid:record_id>/reverse-merge/",
        MPIReverseMergeAPIView.as_view(),
        name="reverse-merge",
    ),
]

__all__ = ("urlpatterns",)

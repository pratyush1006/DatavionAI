"""
Master Patient Index API view exports.
"""

from __future__ import annotations

from apps.patient_management.mpi.api.views.mpi import (
    MPICandidateListAPIView,
    MPICandidateReviewAPIView,
    MPIDetailAPIView,
    MPILifecycleAPIView,
    MPIListCreateAPIView,
    MPIMergeAPIView,
    MPIRestoreAPIView,
    MPIReverseMergeAPIView,
)

__all__ = (
    "MPICandidateListAPIView",
    "MPICandidateReviewAPIView",
    "MPIDetailAPIView",
    "MPIListCreateAPIView",
    "MPILifecycleAPIView",
    "MPIMergeAPIView",
    "MPIReverseMergeAPIView",
    "MPIRestoreAPIView",
)

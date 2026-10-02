"""
Django admin configuration for the Master Patient Index.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.mpi.models import (
    MPIMatchCandidate,
    MPIRecord,
)


@admin.register(MPIRecord)
class MPIRecordAdmin(admin.ModelAdmin):
    """Admin configuration for MPI records."""

    list_display = (
        "enterprise_identifier",
        "patient",
        "organization",
        "status",
        "match_score",
        "confidence",
    )
    list_filter = (
        "status",
        "source_system",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "enterprise_identifier",
        "source_patient_identifier",
        "patient__mrn",
    )


@admin.register(MPIMatchCandidate)
class MPIMatchCandidateAdmin(admin.ModelAdmin):
    """Admin configuration for MPI candidate matches."""

    list_display = (
        "left_record",
        "right_record",
        "score",
        "status",
        "reviewed_at",
    )
    list_filter = ("status",)
    ordering = ("-score",)


__all__ = (
    "MPIMatchCandidateAdmin",
    "MPIRecordAdmin",
)

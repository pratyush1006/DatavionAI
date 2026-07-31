"""
Admin configuration for the Master Patient Index.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)


@admin.register(MasterPatientIndex)
class MasterPatientIndexAdmin(admin.ModelAdmin):
    """Admin for MasterPatientIndex."""

    list_display = (
        "mpi_id",
        "patient",
        "organization",
        "status",
        "verification_status",
        "merge_status",
        "created_at",
    )

    list_filter = (
        "status",
        "verification_status",
        "merge_status",
        "record_source",
    )

    search_fields = (
        "mpi_id",
        "patient__first_name",
        "patient__last_name",
        "patient__patient_number",
        "abha_number",
        "aadhaar_number",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "merged_into",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "organization",
        "patient",
        "merged_into",
    )

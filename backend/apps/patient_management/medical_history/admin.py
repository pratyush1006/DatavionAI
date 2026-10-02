"""Admin."""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.medical_history.models import PatientMedicalHistory


@admin.register(PatientMedicalHistory)
class PatientMedicalHistoryAdmin(admin.ModelAdmin):
    """PatientMedicalHistoryAdmin implementation."""

    list_display = (
        "title",
        "patient",
        "history_type",
        "clinical_status",
        "is_verified",
        "is_active",
        "is_deleted",
        "created_at",
    )
    list_filter = (
        "history_type",
        "clinical_status",
        "is_verified",
        "is_active",
        "is_deleted",
    )
    search_fields = ("title", "description", "recorded_by", "patient__id")
    autocomplete_fields = ("organization", "patient", "verified_by")
    list_select_related = ("organization", "patient", "verified_by")


__all__ = ("PatientMedicalHistoryAdmin",)

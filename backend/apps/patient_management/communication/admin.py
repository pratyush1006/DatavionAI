"""Django admin configuration for Patient Communication."""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.communication.models import PatientCommunication


@admin.register(PatientCommunication)
class PatientCommunicationAdmin(admin.ModelAdmin):
    """Admin configuration for communication records."""

    list_display = (
        "id",
        "patient",
        "channel",
        "direction",
        "status",
        "occurred_at",
        "is_active",
        "is_deleted",
    )
    list_filter = (
        "channel",
        "direction",
        "communication_type",
        "status",
        "is_active",
        "is_deleted",
    )
    search_fields = ("id", "patient__id", "subject", "external_reference")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "deleted_by_id")


__all__ = ("PatientCommunicationAdmin",)

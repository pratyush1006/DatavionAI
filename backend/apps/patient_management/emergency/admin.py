"""Django admin configuration for patient emergency records."""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.emergency.models import EmergencyContact


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """Configure emergency contact administration."""

    list_display = (
        "name",
        "patient",
        "relationship",
        "priority",
        "status",
        "is_deleted",
    )
    list_filter = (
        "relationship",
        "priority",
        "status",
        "is_deleted",
    )
    search_fields = (
        "name",
        "phone",
        "email",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )


__all__ = ("EmergencyContactAdmin",)

"""Django admin configuration for Clinical Appointments."""

from __future__ import annotations

from django.contrib import admin

from apps.clinical.appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Configure Appointment administration."""

    list_display = (
        "appointment_number",
        "patient",
        "provider",
        "appointment_type",
        "status",
        "priority",
        "scheduled_start",
        "scheduled_end",
        "is_active",
        "is_deleted",
    )
    list_filter = (
        "appointment_type",
        "status",
        "priority",
        "is_virtual",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "appointment_number",
        "patient__id",
        "provider__id",
    )
    autocomplete_fields = (
        "organization",
        "patient",
        "provider",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
        "check_in_at",
        "check_out_at",
    )
    ordering = ("-scheduled_start",)
    list_select_related = (
        "organization",
        "patient",
        "provider",
    )


__all__ = ("AppointmentAdmin",)

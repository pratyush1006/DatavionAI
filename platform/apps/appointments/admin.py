"""
Appointment admin configuration.
"""

from django.contrib import admin

from apps.appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for appointments.
    """

    list_display = (
        "appointment_number",
        "patient",
        "provider",
        "appointment_type",
        "status",
        "priority",
        "scheduled_start",
        "is_virtual",
        "is_active",
    )

    list_filter = (
        "appointment_type",
        "status",
        "priority",
        "is_virtual",
        "is_active",
        "organization",
    )

    search_fields = (
        "appointment_number",
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
        "provider__provider_number",
        "provider__employee__user__first_name",
        "provider__employee__user__last_name",
    )

    ordering = (
        "-scheduled_start",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "organization",
        "patient",
        "provider",
        "provider__employee",
        "provider__employee__user",
    )


__all__ = [
    "AppointmentAdmin",
]

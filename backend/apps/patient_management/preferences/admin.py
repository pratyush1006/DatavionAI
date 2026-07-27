"""
Admin configuration for the Patient Preferences module.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)


@admin.register(
    PatientPreference,
)
class PatientPreferenceAdmin(
    admin.ModelAdmin,
):
    """
    Admin configuration for PatientPreference.
    """

    list_display = (
        "patient",
        "language",
        "timezone",
        "portal_theme",
        "status",
        "created_at",
    )

    list_filter = (
        "language",
        "portal_theme",
        "status",
    )

    search_fields = (
        "patient__medical_record_number",
        "patient__first_name",
        "patient__last_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


@admin.register(
    PatientCommunicationPreference,
)
class PatientCommunicationPreferenceAdmin(
    admin.ModelAdmin,
):
    """
    Admin configuration for PatientCommunicationPreference.
    """

    list_display = (
        "patient",
        "channel",
        "priority",
        "enabled",
    )

    list_filter = (
        "channel",
        "enabled",
    )

    search_fields = (
        "patient__medical_record_number",
        "patient__first_name",
        "patient__last_name",
    )

    ordering = ("priority",)

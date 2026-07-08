"""
Admin configuration for the Encounters application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.encounters.models import Encounter


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    """
    Admin configuration for Encounter.
    """

    list_display = (
        "encounter_number",
        "patient",
        "provider",
        "organization",
        "status",
        "started_at",
        "created_at",
    )

    list_filter = (
        "organization",
        "status",
        "is_billable",
        "started_at",
    )

    search_fields = (
        "encounter_number",
        "patient__first_name",
        "patient__last_name",
        "patient__email",
        "provider__employee__first_name",
        "provider__employee__last_name",
        "provider__provider_number",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "appointment",
        "patient",
        "provider",
    )

    list_select_related = (
        "organization",
        "appointment",
        "patient",
        "provider",
    )

    date_hierarchy = "started_at"


__all__ = [
    "EncounterAdmin",
]

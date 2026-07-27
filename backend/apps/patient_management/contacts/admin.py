"""
Admin configuration for patient contacts.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.contacts.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin for Contact."""

    list_display = (
        "value",
        "contact_type",
        "purpose",
        "patient",
        "organization",
        "status",
        "is_primary",
        "is_preferred",
    )

    list_filter = (
        "contact_type",
        "purpose",
        "status",
        "source",
        "is_primary",
        "is_preferred",
    )

    search_fields = (
        "value",
        "patient__first_name",
        "patient__last_name",
    )

    autocomplete_fields = (
        "organization",
        "patient",
    )

    list_select_related = (
        "organization",
        "patient",
    )

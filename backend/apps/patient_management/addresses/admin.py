"""
Admin configuration for patient addresses.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.addresses.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin for Address."""

    list_display = (
        "line_1",
        "city",
        "state",
        "country",
        "address_type",
        "patient",
        "status",
        "is_primary",
    )

    list_filter = (
        "address_type",
        "address_use",
        "status",
        "source",
        "is_primary",
    )

    search_fields = (
        "line_1",
        "city",
        "state",
        "postal_code",
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

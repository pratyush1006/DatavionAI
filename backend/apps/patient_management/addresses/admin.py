"""Patient Address admin."""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.addresses.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "organization",
        "patient",
        "address_type",
        "address_use",
        "status",
        "is_primary",
        "is_verified",
    )
    list_filter = ("address_type", "address_use", "status", "is_primary", "is_verified")
    search_fields = (
        "address_line_1",
        "city_name",
        "region_name",
        "country_name",
        "postal_code",
        "formatted_address",
    )
    autocomplete_fields = (
        "tenant",
        "organization",
        "patient",
        "country",
        "region",
        "city",
        "verified_by",
    )

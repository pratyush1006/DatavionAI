"""
Admin configuration for the Organizations app.
"""

from __future__ import annotations

from django.contrib import admin

from apps.organizations.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Organization.
    """

    list_display = (
        "name",
        "code",
        "organization_type",
        "city",
        "country",
        "email",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "email",
        "city",
    )

    list_filter = (
        "organization_type",
        "country",
        "is_active",
        "created_at",
    )

    ordering = ("name",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "code",
                    "organization_type",
                ),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "phone",
                    "address",
                    "city",
                    "state",
                    "country",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": ("is_active",),
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

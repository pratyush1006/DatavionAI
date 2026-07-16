"""
Admin configuration for the Organizations application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.platform.organizations.models import (
    Organization,
)


@admin.register(
    Organization,
)
class OrganizationAdmin(
    admin.ModelAdmin,
):
    """
    Django admin configuration for Organization.
    """

    list_display = (
        "display_name",
        "code",
        "category",
        "organization_type",
        "status",
        "verification_status",
        "subscription_status",
        "city",
        "country",
        "is_active",
        "is_verified",
        "created_at",
    )

    list_display_links = (
        "display_name",
        "code",
    )

    search_fields = (
        "name",
        "display_name",
        "code",
        "email",
        "support_email",
        "city",
        "state",
        "country",
    )

    list_filter = (
        "category",
        "organization_type",
        "status",
        "verification_status",
        "subscription_status",
        "country",
        "is_active",
        "is_verified",
        "created_at",
    )

    ordering = ("display_name",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Identity",
            {
                "fields": (
                    "name",
                    "display_name",
                    "code",
                    "slug",
                ),
            },
        ),
        (
            "Classification",
            {
                "fields": (
                    "category",
                    "organization_type",
                    "status",
                    "size",
                ),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "support_email",
                    "phone",
                    "website",
                ),
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "country",
                    "postal_code",
                    "timezone",
                ),
            },
        ),
        (
            "Legal Information",
            {
                "fields": (
                    "registration_number",
                    "tax_number",
                    "license_number",
                    "accreditation",
                ),
            },
        ),
        (
            "Platform",
            {
                "fields": (
                    "verification_status",
                    "subscription_status",
                    "is_verified",
                    "is_demo",
                    "is_active",
                ),
            },
        ),
        (
            "Description",
            {
                "fields": ("description",),
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


__all__ = [
    "OrganizationAdmin",
]

"""
Admin configuration for the Organization Hierarchy application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.platform.organizations.models import (
    OrganizationHierarchy,
)


@admin.register(
    OrganizationHierarchy,
)
class OrganizationHierarchyAdmin(
    admin.ModelAdmin,
):
    """
    Django admin configuration for OrganizationHierarchy.
    """

    list_display = (
        "parent_organization",
        "child_organization",
        "relationship_type",
        "status",
        "display_order",
        "effective_from",
        "effective_to",
        "created_at",
    )

    list_display_links = (
        "parent_organization",
        "child_organization",
    )

    search_fields = (
        "parent_organization__name",
        "parent_organization__display_name",
        "parent_organization__code",
        "child_organization__name",
        "child_organization__display_name",
        "child_organization__code",
    )

    list_filter = (
        "relationship_type",
        "status",
        "created_at",
    )

    autocomplete_fields = (
        "parent_organization",
        "child_organization",
    )

    ordering = (
        "parent_organization",
        "display_order",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "parent_organization",
        "child_organization",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Hierarchy",
            {
                "fields": (
                    "parent_organization",
                    "child_organization",
                    "relationship_type",
                    "status",
                    "display_order",
                ),
            },
        ),
        (
            "Effective Period",
            {
                "fields": (
                    "effective_from",
                    "effective_to",
                ),
            },
        ),
        (
            "Additional Information",
            {
                "fields": ("notes",),
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
    "OrganizationHierarchyAdmin",
]

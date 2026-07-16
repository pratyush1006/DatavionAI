"""
Admin configuration for the Departments application.
"""

from __future__ import annotations

from apps.organization.departments.models import Department
from django.contrib import admin


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Department model.
    """

    list_display = (
        "name",
        "organization",
        "code",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "organization__name",
    )

    list_filter = (
        "organization",
        "is_active",
        "created_at",
    )

    ordering = (
        "organization__name",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"


__all__ = [
    "DepartmentAdmin",
]

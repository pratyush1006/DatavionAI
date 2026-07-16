"""
Admin configuration for the Teams application.
"""

from __future__ import annotations

from apps.organization.teams.models import Team
from django.contrib import admin


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Team model.
    """

    list_display = (
        "name",
        "department",
        "code",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "department__name",
    )

    list_filter = (
        "department",
        "is_active",
        "created_at",
    )

    ordering = (
        "department__name",
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
    "TeamAdmin",
]

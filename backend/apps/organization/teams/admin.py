"""
Admin configuration for Teams module.
"""

from django.contrib import admin

from apps.organization.teams.models import (
    Team,
    TeamDepartmentAssignment,
    TeamMember,
    TeamRole,
)


@admin.register(
    Team,
)
class TeamAdmin(
    admin.ModelAdmin,
):
    """
    Team administration.
    """

    list_display = (
        "name",
        "organization",
        "code",
        "team_type",
        "status",
        "is_active",
        "created_at",
    )

    list_filter = (
        "organization",
        "team_type",
        "status",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "organization__name",
    )

    ordering = ("name",)


@admin.register(
    TeamRole,
)
class TeamRoleAdmin(
    admin.ModelAdmin,
):
    """
    Team role administration.
    """

    list_display = (
        "name",
        "team",
        "code",
        "is_lead",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_lead",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "team__name",
    )

    ordering = ("name",)


@admin.register(
    TeamMember,
)
class TeamMemberAdmin(
    admin.ModelAdmin,
):
    """
    Team member administration.

    Team membership is user based.
    Employee integration will be handled
    through HR/Employee bounded context.
    """

    list_display = (
        "team",
        "user",
        "role",
        "status",
        "is_primary",
        "created_at",
    )

    list_filter = (
        "status",
        "is_primary",
        "team",
    )

    search_fields = (
        "team__name",
        "user__email",
    )

    ordering = ("team",)


@admin.register(
    TeamDepartmentAssignment,
)
class TeamDepartmentAssignmentAdmin(
    admin.ModelAdmin,
):
    """
    Team department assignment administration.
    """

    list_display = (
        "team",
        "department",
        "created_at",
    )

    list_filter = (
        "team",
        "department",
    )

    search_fields = (
        "team__name",
        "department__name",
    )

    ordering = (
        "team",
        "department",
    )

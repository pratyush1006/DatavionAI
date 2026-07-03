# Register your models here.
"""
Admin configuration for the RBAC app.
"""

from __future__ import annotations

from django.contrib import admin

from apps.rbac.models import (
    Permission,
    Role,
    RolePermission,
    UserRole,
)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin configuration for Role.
    """

    list_display = (
        "id",
        "name",
        "code",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = ("name",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Permission.
    """

    list_display = (
        "id",
        "name",
        "code",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = ("name",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserRole.
    """

    list_display = (
        "id",
        "user",
        "role",
        "created_at",
    )

    list_filter = (
        "role",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "role__name",
    )

    ordering = ("-created_at",)

    autocomplete_fields = (
        "user",
        "role",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """
    Admin configuration for RolePermission.
    """

    list_display = (
        "id",
        "role",
        "permission",
        "created_at",
    )

    list_filter = (
        "role",
        "created_at",
    )

    search_fields = (
        "role__name",
        "permission__name",
        "permission__code",
    )

    ordering = ("-created_at",)

    autocomplete_fields = (
        "role",
        "permission",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

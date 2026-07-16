"""
Admin configuration for the Accounts application.
"""

from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.platform.accounts.models import (
    Profile,
    User,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the User model.
    """

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )

    list_filter = (
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    ordering = ("email",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = UserAdmin.fieldsets + (
        (
            "Datavion AI",
            {
                "fields": (
                    "is_verified",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.
    """

    list_display = (
        "user",
        "language",
        "timezone",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
    )

    list_filter = (
        "language",
        "timezone",
        "created_at",
    )

    ordering = ("user__email",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"


__all__ = [
    "CustomUserAdmin",
    "ProfileAdmin",
]

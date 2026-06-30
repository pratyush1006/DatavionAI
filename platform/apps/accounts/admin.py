"""
Admin configuration for the Accounts app.
"""

from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import (
    Profile,
    User,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the User model.
    """

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

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
        "phone",
        "language",
        "timezone",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone",
    )

    list_filter = (
        "language",
        "timezone",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

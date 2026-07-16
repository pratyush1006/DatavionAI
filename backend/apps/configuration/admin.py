"""
Admin configuration for the Configuration application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.configuration.models import (
    Configuration,
    FeatureFlag,
)


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Configuration.
    """

    list_display = (
        "key",
        "name",
        "category",
        "value",
        "value_type",
        "is_editable",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "value_type",
        "is_editable",
        "is_active",
    )

    search_fields = (
        "key",
        "name",
        "description",
        "value",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = (
        "category",
        "name",
    )


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    """
    Admin configuration for FeatureFlag.
    """

    list_display = (
        "key",
        "name",
        "is_enabled",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_enabled",
        "is_active",
    )

    search_fields = (
        "key",
        "name",
        "description",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("name",)

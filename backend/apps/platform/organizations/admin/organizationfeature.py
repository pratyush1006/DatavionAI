"""
Admin configuration for the OrganizationFeature model.
"""

from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.platform.organizations.models import OrganizationFeature


@admin.register(OrganizationFeature)
class OrganizationFeatureAdmin(admin.ModelAdmin):
    """
    Django admin configuration for OrganizationFeature.
    """

    list_display = (
        "organization",
        "feature_code",
        "status",
        "enabled_at",
        "disabled_at",
        "created_at",
    )

    list_display_links = (
        "organization",
        "feature_code",
    )

    search_fields = (
        "organization__name",
        "organization__display_name",
        "organization__code",
        "feature_code",
    )

    list_filter = (
        "status",
        "created_at",
        "enabled_at",
        "disabled_at",
    )

    autocomplete_fields = ("organization",)

    ordering = (
        "organization",
        "feature_code",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    list_select_related = ("organization",)

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    save_on_top = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Organization",
            {
                "fields": ("organization",),
            },
        ),
        (
            "Feature",
            {
                "fields": (
                    "feature_code",
                    "status",
                ),
            },
        ),
        (
            "Configuration",
            {
                "fields": ("settings",),
            },
        ),
        (
            "Lifecycle",
            {
                "fields": (
                    "enabled_at",
                    "disabled_at",
                ),
            },
        ),
        (
            "Audit",
            {
                "classes": ("collapse",),
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    actions = (
        "enable_features",
        "disable_features",
    )

    def get_queryset(
        self,
        request: HttpRequest,
    ) -> QuerySet[OrganizationFeature]:
        """
        Return an optimized queryset for the admin.
        """
        return super().get_queryset(request).select_related("organization")

    @admin.action(description="Enable selected organization features")
    def enable_features(
        self,
        request: HttpRequest,
        queryset: QuerySet[OrganizationFeature],
    ) -> None:
        """
        Enable the selected feature entitlements.
        """
        queryset.update(
            status=OrganizationFeature.FeatureStatus.ENABLED,
        )

    @admin.action(description="Disable selected organization features")
    def disable_features(
        self,
        request: HttpRequest,
        queryset: QuerySet[OrganizationFeature],
    ) -> None:
        """
        Disable the selected feature entitlements.
        """
        queryset.update(
            status=OrganizationFeature.FeatureStatus.DISABLED,
        )


__all__: tuple[str, ...] = ("OrganizationFeatureAdmin",)

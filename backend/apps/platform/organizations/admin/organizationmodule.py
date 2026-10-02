"""
Admin configuration for the OrganizationModule model.
"""

from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.platform.organizations.models import OrganizationModule


@admin.register(OrganizationModule)
class OrganizationModuleAdmin(admin.ModelAdmin):
    """
    Django admin configuration for OrganizationModule.
    """

    list_display = (
        "organization",
        "module_code",
        "status",
        "enabled_at",
        "disabled_at",
        "created_at",
    )

    list_display_links = (
        "organization",
        "module_code",
    )

    search_fields = (
        "organization__name",
        "organization__display_name",
        "organization__code",
        "module_code",
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
        "module_code",
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

    actions = (
        "enable_modules",
        "disable_modules",
    )

    fieldsets = (
        (
            "Organization",
            {
                "fields": ("organization",),
            },
        ),
        (
            "Module",
            {
                "fields": (
                    "module_code",
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

    def get_queryset(
        self,
        request: HttpRequest,
    ) -> QuerySet[OrganizationModule]:
        """
        Return an optimized queryset for the admin.
        """
        return super().get_queryset(request).select_related("organization")

    @admin.action(description="Enable selected organization modules")
    def enable_modules(
        self,
        request: HttpRequest,
        queryset: QuerySet[OrganizationModule],
    ) -> None:
        """
        Enable the selected module entitlements.
        """
        queryset.update(
            status=OrganizationModule.Status.ENABLED,
        )

    @admin.action(description="Disable selected organization modules")
    def disable_modules(
        self,
        request: HttpRequest,
        queryset: QuerySet[OrganizationModule],
    ) -> None:
        """
        Disable the selected module entitlements.
        """
        queryset.update(
            status=OrganizationModule.Status.DISABLED,
        )


__all__: tuple[str, ...] = ("OrganizationModuleAdmin",)

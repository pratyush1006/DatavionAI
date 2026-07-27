"""
Admin configuration for the OrganizationSettings model.
"""

from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.platform.organizations.models import OrganizationSettings


@admin.register(OrganizationSettings)
class OrganizationSettingsAdmin(admin.ModelAdmin):
    """
    Django admin configuration for OrganizationSettings.
    """

    list_display = (
        "organization",
        "language",
        "timezone",
        "currency",
        "email_notifications",
        "sms_notifications",
        "push_notifications",
        "mfa_required",
        "created_at",
    )

    list_display_links = ("organization",)

    search_fields = (
        "organization__name",
        "organization__display_name",
        "organization__code",
        "language",
        "timezone",
        "currency",
        "default_dashboard",
    )

    list_filter = (
        "language",
        "timezone",
        "currency",
        "email_notifications",
        "sms_notifications",
        "push_notifications",
        "mfa_required",
        "created_at",
    )

    autocomplete_fields = ("organization",)

    ordering = ("organization",)

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
            "Localization",
            {
                "fields": (
                    "language",
                    "timezone",
                    "currency",
                    "date_format",
                    "time_format",
                ),
            },
        ),
        (
            "Notifications",
            {
                "fields": (
                    "email_notifications",
                    "sms_notifications",
                    "push_notifications",
                ),
            },
        ),
        (
            "Security",
            {
                "fields": (
                    "session_timeout_minutes",
                    "mfa_required",
                ),
            },
        ),
        (
            "Dashboard",
            {
                "fields": ("default_dashboard",),
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
    ) -> QuerySet[OrganizationSettings]:
        """
        Return an optimized queryset for the admin.
        """
        return super().get_queryset(request).select_related("organization")


__all__: tuple[str, ...] = ("OrganizationSettingsAdmin",)

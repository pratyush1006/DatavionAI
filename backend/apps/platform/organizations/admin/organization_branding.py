"""
Admin configuration for the Organization Branding application.
"""

from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.platform.organizations.models import OrganizationBranding


@admin.register(OrganizationBranding)
class OrganizationBrandingAdmin(admin.ModelAdmin):
    """
    Django admin configuration for OrganizationBranding.
    """

    list_display = (
        "organization",
        "theme_mode",
        "primary_color",
        "custom_domain",
        "created_at",
    )

    list_display_links = ("organization",)

    search_fields = (
        "organization__name",
        "organization__display_name",
        "organization__code",
        "custom_domain",
    )

    list_filter = (
        "theme_mode",
        "created_at",
    )

    autocomplete_fields = ("organization",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    list_select_related = ("organization",)

    list_per_page = 25

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
            "Visual Identity",
            {
                "fields": (
                    "logo",
                    "favicon",
                    "primary_color",
                    "secondary_color",
                    "accent_color",
                    "font_family",
                    "theme_mode",
                ),
            },
        ),
        (
            "Login & Domain",
            {
                "fields": (
                    "custom_domain",
                    "login_message",
                ),
            },
        ),
        (
            "Email",
            {
                "fields": ("email_footer_text",),
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
    ) -> QuerySet[OrganizationBranding]:
        """
        Return an optimized queryset for the admin.
        """
        return super().get_queryset(request).select_related("organization")


__all__: tuple[str, ...] = ("OrganizationBrandingAdmin",)

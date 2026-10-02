"""
Admin configuration for the OrganizationProfile model.
"""

from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.platform.organizations.models import OrganizationProfile


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    """
    Django admin configuration for OrganizationProfile.
    """

    list_display = (
        "organization",
        "industry",
        "facility_type",
        "employee_count",
        "bed_capacity",
        "established_year",
        "created_at",
    )

    list_display_links = ("organization",)

    search_fields = (
        "organization__name",
        "organization__display_name",
        "organization__code",
        "license_number",
    )

    list_filter = (
        "industry",
        "facility_type",
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
            "Classification",
            {
                "fields": (
                    "industry",
                    "facility_type",
                ),
            },
        ),
        (
            "Profile",
            {
                "fields": (
                    "description",
                    "established_year",
                    "employee_count",
                    "bed_capacity",
                    "license_number",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("metadata",),
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
    ) -> QuerySet[OrganizationProfile]:
        """
        Return an optimized queryset for the admin.
        """
        return super().get_queryset(request).select_related("organization")


__all__: tuple[str, ...] = ("OrganizationProfileAdmin",)

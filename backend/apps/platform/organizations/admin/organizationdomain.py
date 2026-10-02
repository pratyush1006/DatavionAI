"""
Admin configuration for the OrganizationDomain model.
"""

from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.platform.organizations.models import OrganizationDomain


@admin.register(OrganizationDomain)
class OrganizationDomainAdmin(admin.ModelAdmin):
    """
    Django admin configuration for OrganizationDomain.
    """

    list_display = (
        "organization",
        "domain",
        "is_primary",
        "verification_status",
        "is_verified",
        "is_active",
        "created_at",
    )

    list_display_links = (
        "organization",
        "domain",
    )

    search_fields = (
        "organization__name",
        "organization__display_name",
        "organization__code",
        "domain",
    )

    list_filter = (
        "verification_status",
        "is_primary",
        "is_verified",
        "is_active",
        "created_at",
    )

    autocomplete_fields = ("organization",)

    ordering = (
        "organization",
        "domain",
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
        "verify_domains",
        "unverify_domains",
    )

    fieldsets = (
        (
            "Organization",
            {
                "fields": ("organization",),
            },
        ),
        (
            "Domain",
            {
                "fields": (
                    "domain",
                    "is_primary",
                ),
            },
        ),
        (
            "Verification",
            {
                "fields": (
                    "verification_status",
                    "is_verified",
                    "is_active",
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
    ) -> QuerySet[OrganizationDomain]:
        """
        Return an optimized queryset for the admin.
        """
        return super().get_queryset(request).select_related("organization")

    @admin.action(description="Mark selected domains as verified")
    def verify_domains(
        self,
        request: HttpRequest,
        queryset: QuerySet[OrganizationDomain],
    ) -> None:
        queryset.update(
            is_verified=True,
        )

    @admin.action(description="Mark selected domains as unverified")
    def unverify_domains(
        self,
        request: HttpRequest,
        queryset: QuerySet[OrganizationDomain],
    ) -> None:
        queryset.update(
            is_verified=False,
        )


__all__: tuple[str, ...] = ("OrganizationDomainAdmin",)

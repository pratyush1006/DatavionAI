"""
Admin configuration for the Organizations application.
"""

from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.platform.organizations.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Organization.
    """

    list_display = (
        "display_name",
        "code",
        "category",
        "organization_type",
        "status",
        "verification_status",
        "city",
        "country",
        "is_active",
        "created_at",
    )

    list_display_links = (
        "display_name",
        "code",
    )

    list_editable = ("is_active",)

    search_fields = (
        "name",
        "display_name",
        "code",
        "slug",
        "email",
        "support_email",
        "city",
        "state",
        "country",
        "registration_number",
    )

    list_filter = (
        "category",
        "organization_type",
        "status",
        "verification_status",
        "country",
        "is_active",
        "created_at",
    )

    ordering = ("display_name",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    list_per_page = 25

    preserve_filters = True

    save_on_top = True

    empty_value_display = "-"

    actions = (
        "activate_organizations",
        "deactivate_organizations",
    )

    fieldsets = (
        (
            "Identity",
            {
                "fields": (
                    "name",
                    "display_name",
                    "code",
                    "slug",
                ),
            },
        ),
        (
            "Classification",
            {
                "fields": (
                    "category",
                    "organization_type",
                    "status",
                    "size",
                ),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "support_email",
                    "phone",
                    "website",
                ),
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "country",
                    "postal_code",
                    "timezone",
                ),
            },
        ),
        (
            "Legal Information",
            {
                "fields": (
                    "registration_number",
                    "tax_number",
                    "license_number",
                    "accreditation",
                ),
            },
        ),
        (
            "Platform",
            {
                "fields": (
                    "verification_status",
                    "is_demo",
                    "is_active",
                ),
            },
        ),
        (
            "Description",
            {
                "fields": ("description",),
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
    ) -> QuerySet[Organization]:
        """
        Return the optimized queryset for the admin.

        Add select_related() here if any of the displayed fields become
        ForeignKey relationships in the future.
        """
        queryset = super().get_queryset(request)

        return queryset

    @admin.action(description="Activate selected organizations")
    def activate_organizations(
        self,
        request: HttpRequest,
        queryset: QuerySet[Organization],
    ) -> None:
        """
        Activate the selected organizations.
        """
        queryset.update(
            is_active=True,
        )

    @admin.action(description="Deactivate selected organizations")
    def deactivate_organizations(
        self,
        request: HttpRequest,
        queryset: QuerySet[Organization],
    ) -> None:
        """
        Deactivate the selected organizations.
        """
        queryset.update(
            is_active=False,
        )


__all__: tuple[str, ...] = ("OrganizationAdmin",)

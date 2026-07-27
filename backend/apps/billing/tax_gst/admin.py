"""
Admin configuration for the Tax Gst application.
"""

from __future__ import annotations

from apps.billing.tax_gst.models import (
    TaxFiling,
    TaxRate,
)
from django.contrib import admin


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    """
    Django admin configuration for TaxRate.
    """

    list_display = (
        "id",
        "code",
        "name",
        "rate",
        "tax_type",
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "code",
    )

    list_filter = (
        "organization",
        "tax_type",
        "is_active",
        "created_at",
    )

    ordering = ("name",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("organization",)

    list_select_related = ("organization",)

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"


@admin.register(TaxFiling)
class TaxFilingAdmin(admin.ModelAdmin):
    """
    Django admin configuration for TaxFiling.
    """

    list_display = (
        "id",
        "period",
        "tax_rate",
        "status",
        "is_active",
        "created_at",
    )
    search_fields = (
        "period",
        "reference",
    )

    list_filter = (
        "organization",
        "status",
        "is_active",
        "created_at",
    )

    ordering = ("-period_end",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("organization",)

    list_select_related = ("organization",)

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"


__all__ = [
    "TaxRateAdmin",
    "TaxFilingAdmin",
]

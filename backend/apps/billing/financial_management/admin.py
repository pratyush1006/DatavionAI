"""
Admin configuration for the Financial Management application.
"""

from __future__ import annotations

from apps.billing.financial_management.models import (
    Budget,
    FinancialReport,
)
from django.contrib import admin


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Budget.
    """

    list_display = (
        "id",
        "name",
        "fiscal_year",
        "status",
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "fiscal_year",
    )

    list_filter = (
        "organization",
        "status",
        "is_active",
        "created_at",
    )

    ordering = (
        "fiscal_year",
        "name",
    )

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


@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    """
    Django admin configuration for FinancialReport.
    """

    list_display = (
        "id",
        "title",
        "report_type",
        "status",
        "is_active",
        "created_at",
    )
    search_fields = (
        "title",
        "report_type",
    )

    list_filter = (
        "organization",
        "report_type",
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
    "BudgetAdmin",
    "FinancialReportAdmin",
]

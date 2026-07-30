"""
Admin configuration for the Accounts Payable application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.billing.accounts_payable.models import (
    Vendor,
    VendorInvoice,
)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Vendor.
    """

    list_display = (
        "id",
        "code",
        "name",
        "email",
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "code",
        "email",
        "tax_id",
    )

    list_filter = (
        "organization",
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


@admin.register(VendorInvoice)
class VendorInvoiceAdmin(admin.ModelAdmin):
    """
    Django admin configuration for VendorInvoice.
    """

    list_display = (
        "id",
        "invoice_number",
        "vendor",
        "amount",
        "due_date",
        "status",
        "is_active",
        "created_at",
    )
    search_fields = (
        "invoice_number",
        "reference",
    )

    list_filter = (
        "organization",
        "status",
        "is_active",
        "created_at",
    )

    ordering = ("-due_date",)

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
    "VendorAdmin",
    "VendorInvoiceAdmin",
]

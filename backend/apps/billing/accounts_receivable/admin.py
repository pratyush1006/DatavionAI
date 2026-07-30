"""
Admin configuration for the Accounts Receivable application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.billing.accounts_receivable.models import (
    Customer,
    CustomerInvoice,
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Customer.
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


@admin.register(CustomerInvoice)
class CustomerInvoiceAdmin(admin.ModelAdmin):
    """
    Django admin configuration for CustomerInvoice.
    """

    list_display = (
        "id",
        "invoice_number",
        "customer",
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
    "CustomerAdmin",
    "CustomerInvoiceAdmin",
]

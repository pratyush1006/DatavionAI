"""Django admin configuration for Accounts Receivable."""

from __future__ import annotations

from django.contrib import admin

from .models import ARAccount, ARActivityLog, ARTransaction


@admin.register(ARAccount)
class ARAccountAdmin(admin.ModelAdmin):
    """Admin configuration for AR accounts."""

    list_display = (
        "account_number",
        "organization",
        "patient",
        "status",
        "balance_amount",
        "currency",
    )
    list_filter = ("status", "currency")
    search_fields = ("account_number", "patient__mrn", "patient__first_name")
    readonly_fields = (
        "balance_amount",
        "total_charges",
        "total_payments",
        "total_adjustments",
        "total_write_offs",
        "version",
        "opened_at",
        "closed_at",
        "created_at",
        "updated_at",
    )


@admin.register(ARTransaction)
class ARTransactionAdmin(admin.ModelAdmin):
    """Admin configuration for AR transactions."""

    list_display = (
        "transaction_number",
        "account",
        "transaction_type",
        "status",
        "amount",
        "transaction_date",
    )
    list_filter = ("transaction_type", "status")
    search_fields = ("transaction_number", "external_reference")
    readonly_fields = (
        "created_at",
        "updated_at",
        "reversed_at",
        "reversed_by",
    )


@admin.register(ARActivityLog)
class ARActivityLogAdmin(admin.ModelAdmin):
    """Admin configuration for AR audit records."""

    list_display = ("account", "action", "performed_by", "performed_at")
    list_filter = ("action",)
    readonly_fields = (
        "organization",
        "account",
        "action",
        "details",
        "performed_by",
        "performed_at",
        "created_at",
        "updated_at",
    )


__all__ = ("ARAccountAdmin", "ARActivityLogAdmin", "ARTransactionAdmin")

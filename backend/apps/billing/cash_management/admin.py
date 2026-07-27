"""
Admin configuration for the Cash Management application.
"""

from __future__ import annotations

from apps.billing.cash_management.models import (
    BankAccount,
    CashTransaction,
)
from django.contrib import admin


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    """
    Django admin configuration for BankAccount.
    """

    list_display = (
        "id",
        "name",
        "bank_name",
        "currency",
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "account_number",
        "bank_name",
    )

    list_filter = (
        "organization",
        "currency",
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


@admin.register(CashTransaction)
class CashTransactionAdmin(admin.ModelAdmin):
    """
    Django admin configuration for CashTransaction.
    """

    list_display = (
        "id",
        "reference",
        "bank_account",
        "amount",
        "transaction_type",
        "is_active",
        "created_at",
    )
    search_fields = (
        "reference",
        "description",
    )

    list_filter = (
        "organization",
        "transaction_type",
        "is_active",
        "created_at",
    )

    ordering = ("-transaction_date",)

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
    "BankAccountAdmin",
    "CashTransactionAdmin",
]

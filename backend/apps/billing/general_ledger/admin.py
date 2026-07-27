"""
Admin configuration for the General Ledger application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.billing.general_ledger.models import (
    GeneralLedgerAccount,
    GeneralLedgerJournalEntry,
)


@admin.register(GeneralLedgerAccount)
class GeneralLedgerAccountAdmin(admin.ModelAdmin):
    """
    Django admin configuration for GeneralLedgerAccount.
    """

    list_display = (
        "code",
        "name",
        "organization",
        "account_type",
        "status",
        "is_active",
        "created_at",
    )

    search_fields = (
        "code",
        "name",
        "description",
    )

    list_filter = (
        "organization",
        "account_type",
        "status",
        "is_active",
        "created_at",
    )

    ordering = (
        "code",
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


@admin.register(GeneralLedgerJournalEntry)
class GeneralLedgerJournalEntryAdmin(admin.ModelAdmin):
    """
    Django admin configuration for GeneralLedgerJournalEntry.
    """

    list_display = (
        "reference",
        "account",
        "entry_type",
        "amount",
        "posted_at",
        "is_active",
        "created_at",
    )

    search_fields = (
        "reference",
        "description",
    )

    list_filter = (
        "entry_type",
        "posted_at",
        "is_active",
        "created_at",
    )

    ordering = ("-posted_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "account",
    )

    list_select_related = (
        "organization",
        "account",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"


__all__ = [
    "GeneralLedgerAccountAdmin",
    "GeneralLedgerJournalEntryAdmin",
]

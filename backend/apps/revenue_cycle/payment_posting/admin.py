"""Django admin configuration for payment posting."""

from __future__ import annotations

from django.contrib import admin

from .models import PaymentPosting


@admin.register(PaymentPosting)
class PaymentPostingAdmin(admin.ModelAdmin):
    """Admin configuration for payment postings."""

    list_display = (
        "id",
        "organization",
        "patient",
        "payer_name",
        "amount",
        "status",
        "source",
        "posted_at",
        "created_at",
    )
    list_filter = ("status", "source", "is_deleted")
    search_fields = (
        "id",
        "payer_name",
        "payer_claim_reference",
        "external_reference",
        "idempotency_key",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "posted_at",
        "reversed_at",
    )


__all__ = ("PaymentPostingAdmin",)

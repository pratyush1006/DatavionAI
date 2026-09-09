"""Django admin configuration for ERA."""

from __future__ import annotations

from django.contrib import admin

from .models import ERA


@admin.register(ERA)
class ERAAdmin(admin.ModelAdmin):
    """Configure administrative ERA display."""

    list_display = (
        "id",
        "organization",
        "payer_name",
        "trace_number",
        "payment_amount",
        "status",
        "received_at",
    )
    list_filter = ("status", "source", "is_deleted")
    search_fields = (
        "trace_number",
        "payer_name",
        "payer_identifier",
        "external_reference",
        "idempotency_key",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "validated_at",
        "posted_at",
        "reversed_at",
    )


__all__ = ("ERAAdmin",)

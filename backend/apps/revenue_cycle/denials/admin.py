"""Django admin for Revenue Cycle Denials."""

from __future__ import annotations

from django.contrib import admin

from .models import Denial


@admin.register(Denial)
class DenialAdmin(admin.ModelAdmin):
    """Configure denial administration."""

    list_display = (
        "id",
        "organization",
        "patient",
        "payer_name",
        "denial_code",
        "amount",
        "status",
        "priority",
        "received_at",
    )
    list_filter = ("status", "priority")
    search_fields = (
        "external_claim_id",
        "denial_code",
        "denial_reason",
        "external_reference",
    )
    readonly_fields = ("id", "created_at", "updated_at", "resolved_at")


__all__ = ("DenialAdmin",)

"""
Django admin configuration for Revenue Cycle Appeals.
"""

from __future__ import annotations

from django.contrib import admin

from apps.revenue_cycle.appeals.models import Appeal


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    """Configure the Revenue Cycle Appeal administration view."""

    list_display = (
        "appeal_number",
        "claim_reference",
        "payer_name",
        "status",
        "requested_amount",
        "approved_amount",
        "created_at",
    )
    list_filter = (
        "status",
        "priority",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "appeal_number",
        "claim_reference",
        "payer_name",
        "denial_reference",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "submitted_at",
        "decided_at",
    )


__all__ = ("AppealAdmin",)

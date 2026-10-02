"""Django admin configuration for Revenue Analytics."""

from __future__ import annotations

from django.contrib import admin

from .models import RevenueMetricSnapshot


@admin.register(RevenueMetricSnapshot)
class RevenueMetricSnapshotAdmin(admin.ModelAdmin):
    """Admin configuration for analytics snapshots."""

    list_display = (
        "organization",
        "period",
        "period_start",
        "period_end",
        "gross_charges",
        "payments",
        "outstanding_ar",
        "generated_at",
    )
    list_filter = ("period",)
    search_fields = ("organization__name",)
    readonly_fields = (
        "organization",
        "period",
        "period_start",
        "period_end",
        "gross_charges",
        "payments",
        "adjustments",
        "denials",
        "write_offs",
        "outstanding_ar",
        "encounter_count",
        "claim_count",
        "denied_claim_count",
        "paid_claim_count",
        "generated_at",
        "created_at",
        "updated_at",
    )


__all__ = ("RevenueMetricSnapshotAdmin",)

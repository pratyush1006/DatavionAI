"""Django admin for Revenue Cycle Eligibility."""

from __future__ import annotations

from django.contrib import admin

from apps.revenue_cycle.eligibility.models import Eligibility


@admin.register(Eligibility)
class EligibilityAdmin(admin.ModelAdmin):
    """Admin interface for Eligibility records."""

    list_display = (
        "request_reference",
        "patient",
        "payer_id",
        "member_id",
        "status",
        "coverage_status",
        "requested_at",
    )
    list_filter = ("status", "coverage_status", "is_active", "is_deleted")
    search_fields = (
        "request_reference",
        "payer_id",
        "member_id",
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
    )
    readonly_fields = ("id", "requested_at", "verified_at", "created_at", "updated_at")
    list_select_related = ("patient", "organization", "verified_by")


__all__ = ("EligibilityAdmin",)

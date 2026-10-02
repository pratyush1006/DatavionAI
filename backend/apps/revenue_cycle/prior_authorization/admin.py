"""Django admin for Revenue Cycle Prior Authorization."""

from __future__ import annotations

from django.contrib import admin

from apps.revenue_cycle.prior_authorization.models import PriorAuthorization


@admin.register(PriorAuthorization)
class PriorAuthorizationAdmin(admin.ModelAdmin):
    """Admin interface for Prior Authorization records."""

    list_display = (
        "request_reference",
        "patient",
        "payer_id",
        "member_id",
        "status",
        "outcome",
        "requested_at",
    )
    list_filter = (
        "status",
        "outcome",
        "verification_method",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "request_reference",
        "payer_id",
        "member_id",
        "policy_number",
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
    )
    readonly_fields = (
        "id",
        "requested_at",
        "verified_at",
        "created_at",
        "updated_at",
    )
    list_select_related = ("patient", "organization", "verified_by")


__all__ = ("PriorAuthorizationAdmin",)

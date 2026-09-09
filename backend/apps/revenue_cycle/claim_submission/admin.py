"""Django admin configuration for claim submission."""

from __future__ import annotations

from django.contrib import admin

from apps.revenue_cycle.claim_submission.models import ClaimSubmission


@admin.register(ClaimSubmission)
class ClaimSubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for claim submissions."""

    list_display = (
        "claim_reference",
        "payer_id",
        "patient",
        "organization",
        "status",
        "created_at",
    )
    list_filter = ("status", "submission_method", "is_deleted")
    search_fields = (
        "claim_reference",
        "payer_id",
        "external_submission_id",
        "idempotency_key",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "submitted_at",
        "accepted_at",
        "failed_at",
        "cancelled_at",
    )


__all__ = ("ClaimSubmissionAdmin",)

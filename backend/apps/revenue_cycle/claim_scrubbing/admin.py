"""Django admin configuration for claim scrubbing."""

from __future__ import annotations

from django.contrib import admin

from apps.revenue_cycle.claim_scrubbing.models import (
    ClaimScrub,
    ClaimScrubFinding,
    ScrubRule,
)


@admin.register(ScrubRule)
class ScrubRuleAdmin(admin.ModelAdmin):
    """Admin configuration for scrub rules."""

    list_display = (
        "code",
        "name",
        "organization",
        "rule_type",
        "is_blocking",
        "is_active",
    )
    list_filter = ("rule_type", "is_blocking", "is_active")
    search_fields = ("code", "name")


@admin.register(ClaimScrub)
class ClaimScrubAdmin(admin.ModelAdmin):
    """Admin configuration for scrub executions."""

    list_display = (
        "claim_reference",
        "patient",
        "organization",
        "status",
        "created_at",
    )
    list_filter = ("status", "is_deleted")
    search_fields = ("claim_reference", "idempotency_key")
    readonly_fields = ("id", "created_at", "updated_at", "started_at", "completed_at")


@admin.register(ClaimScrubFinding)
class ClaimScrubFindingAdmin(admin.ModelAdmin):
    """Admin configuration for scrub findings."""

    list_display = ("scrub", "rule", "severity", "is_blocking", "is_resolved")
    list_filter = ("severity", "is_blocking", "is_resolved")


__all__ = ("ScrubRuleAdmin", "ClaimScrubAdmin", "ClaimScrubFindingAdmin")

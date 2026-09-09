"""Django admin configuration for Revenue Cycle integration."""

from __future__ import annotations

from django.contrib import admin

from .models import RevenueCycleIntegrationRecord


@admin.register(RevenueCycleIntegrationRecord)
class RevenueCycleIntegrationRecordAdmin(admin.ModelAdmin):
    """Admin configuration for integration records."""

    list_display = (
        "event_name",
        "organization",
        "source",
        "event_type",
        "status",
        "attempts",
        "created_at",
        "processed_at",
    )
    list_filter = ("source", "event_type", "status")
    search_fields = (
        "event_name",
        "idempotency_key",
        "last_error",
    )
    readonly_fields = (
        "organization",
        "event_type",
        "source",
        "event_name",
        "aggregate_id",
        "idempotency_key",
        "payload",
        "status",
        "attempts",
        "last_error",
        "processed_at",
        "created_by",
        "created_at",
        "updated_at",
    )


__all__ = ("RevenueCycleIntegrationRecordAdmin",)

"""Django admin configuration for Charge Capture."""

from __future__ import annotations

from django.contrib import admin

from .models import Charge

__all__ = ("ChargeAdmin",)


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    """Provide operational administration for charges."""

    list_display = (
        "id",
        "service_code",
        "patient",
        "organization",
        "status",
        "total_amount",
        "created_at",
    )
    list_filter = ("status", "is_active", "is_deleted")
    search_fields = (
        "service_code",
        "description",
        "idempotency_key",
        "patient__id",
    )
    readonly_fields = (
        "id",
        "total_amount",
        "created_at",
        "updated_at",
        "captured_at",
        "voided_at",
    )

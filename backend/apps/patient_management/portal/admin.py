"""
Django admin configuration for Patient Portal.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.portal.models import PatientPortalAccount


@admin.register(PatientPortalAccount)
class PatientPortalAccountAdmin(admin.ModelAdmin):
    """Admin configuration for Patient Portal accounts."""

    list_display = (
        "username",
        "patient",
        "organization",
        "status",
        "auth_provider",
        "email_verified",
        "two_factor_enabled",
    )
    list_filter = (
        "status",
        "auth_provider",
        "email_verified",
        "two_factor_enabled",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "username",
        "email",
        "patient__mrn",
    )
    ordering = ("username",)


__all__ = ("PatientPortalAccountAdmin",)

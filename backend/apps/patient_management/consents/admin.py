"""
Django admin configuration for Patient Consents.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.consents.models import (
    PatientConsent,
)


@admin.register(PatientConsent)
class PatientConsentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Patient Consent records.
    """

    list_display = (
        "id",
        "patient",
        "organization",
        "purpose",
        "status",
        "granted_at",
        "expires_at",
    )
    list_filter = (
        "purpose",
        "status",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "id",
        "patient__id",
        "evidence_reference",
    )
    ordering = ("-created_at",)


__all__ = ("PatientConsentAdmin",)

"""
Django admin configuration for Patient Referrals.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.referrals.models import PatientReferral


@admin.register(PatientReferral)
class PatientReferralAdmin(admin.ModelAdmin):
    """Configure administrative referral management."""

    list_display = (
        "referral_number",
        "patient",
        "referred_to",
        "priority",
        "urgency",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "priority",
        "urgency",
    )
    search_fields = (
        "referral_number",
        "referred_to",
        "patient__mrn",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "accepted_at",
        "completed_at",
        "created_by_id",
        "updated_by_id",
    )


__all__ = ("PatientReferralAdmin",)

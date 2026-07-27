"""
Admin configuration for the Patient Consents module.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.consents.models import (
    Consent,
)

__all__ = [
    "ConsentAdmin",
]


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    """
    Admin interface for Consent.
    """

    list_display = (
        "consent_number",
        "patient",
        "consent_type",
        "status",
        "version",
        "is_active",
        "effective_date",
        "expiry_date",
        "created_at",
    )

    list_filter = (
        "consent_type",
        "status",
        "method",
        "source",
        "is_active",
        "is_required",
    )

    search_fields = (
        "consent_number",
        "title",
        "patient__patient_number",
        "patient__first_name",
        "patient__last_name",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "doctor",
        "guardian",
        "requested_by",
        "approved_by",
        "document",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    list_select_related = (
        "organization",
        "patient",
        "doctor",
    )

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Consent",
            {
                "fields": (
                    "organization",
                    "patient",
                    "consent_number",
                    "title",
                    "description",
                    "consent_type",
                    "status",
                    "version",
                ),
            },
        ),
        (
            "Workflow",
            {
                "fields": (
                    "method",
                    "source",
                    "requested_by",
                    "approved_by",
                    "doctor",
                    "guardian",
                ),
            },
        ),
        (
            "Validity",
            {
                "fields": (
                    "effective_date",
                    "expiry_date",
                    "granted_at",
                    "revoked_at",
                    "withdrawn_at",
                ),
            },
        ),
        (
            "Document",
            {
                "fields": (
                    "document",
                    "remarks",
                ),
            },
        ),
        (
            "Configuration",
            {
                "fields": (
                    "is_required",
                    "is_active",
                ),
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

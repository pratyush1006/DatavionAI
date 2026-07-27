# apps/patient_management/identifiers/admin.py

"""
Admin configuration for patient identifiers.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.identifiers.models import (
    IdentifierVerification,
    PatientIdentifier,
)


@admin.register(PatientIdentifier)
class PatientIdentifierAdmin(admin.ModelAdmin):
    """Admin for PatientIdentifier."""

    list_display = (
        "identifier_value",
        "identifier_type",
        "patient",
        "organization",
        "status",
        "verification_status",
        "is_primary",
        "created_at",
    )

    list_filter = (
        "identifier_type",
        "status",
        "verification_status",
        "is_primary",
        "source",
        "organization",
    )

    search_fields = (
        "identifier_value",
        "display_value",
        "patient__medical_record_number",
        "patient__first_name",
        "patient__last_name",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "verified_by",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "verified_at",
    )

    ordering = (
        "patient",
        "identifier_type",
    )

    list_select_related = (
        "organization",
        "patient",
        "verified_by",
    )


@admin.register(IdentifierVerification)
class IdentifierVerificationAdmin(admin.ModelAdmin):
    """Admin for IdentifierVerification."""

    list_display = (
        "identifier",
        "status",
        "verification_source",
        "verified_by",
        "verified_at",
        "created_at",
    )

    list_filter = (
        "status",
        "verification_source",
    )

    search_fields = (
        "identifier__identifier_value",
        "reference_number",
    )

    autocomplete_fields = (
        "identifier",
        "verified_by",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "identifier",
        "verified_by",
    )

"""
Django admin configuration for the canonical Patient model.

The Patient model is owned by the Patient Management bounded context.
This module intentionally contains the canonical PatientAdmin registration
so Django Admin can resolve all relationships to patient_core.Patient.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.patients.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for the canonical Patient model.
    """

    list_display = (
        "mrn",
        "display_name",
        "organization",
        "gender",
        "phone",
        "status",
        "is_active",
        "created_at",
    )

    search_fields = (
        "mrn",
        "first_name",
        "middle_name",
        "last_name",
        "preferred_name",
        "phone",
        "email",
    )

    list_filter = (
        "organization",
        "gender",
        "status",
        "blood_group",
        "is_active",
        "created_at",
    )

    ordering = (
        "last_name",
        "first_name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("organization",)

    list_select_related = ("organization",)

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Patient Information",
            {
                "fields": (
                    "organization",
                    "mrn",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "preferred_name",
                ),
            },
        ),
        (
            "Demographics",
            {
                "fields": (
                    "date_of_birth",
                    "gender",
                    "marital_status",
                    "blood_group",
                ),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "phone",
                    "email",
                    "address",
                    "city",
                    "state",
                    "country",
                    "postal_code",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "is_active",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


__all__ = ("PatientAdmin",)

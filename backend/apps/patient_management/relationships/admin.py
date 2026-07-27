"""
Admin configuration for Patient Relationships.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


@admin.register(PatientRelationship)
class PatientRelationshipAdmin(admin.ModelAdmin):
    """Admin for PatientRelationship."""

    list_display = (
        "patient",
        "related_patient",
        "relationship_type",
        "status",
        "verification_status",
        "is_primary",
        "created_at",
    )

    list_filter = (
        "relationship_type",
        "status",
        "verification_status",
        "source",
        "is_primary",
    )

    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "related_patient__first_name",
        "related_patient__last_name",
        "relationship_name",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "related_patient",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "organization",
        "patient",
        "related_patient",
    )

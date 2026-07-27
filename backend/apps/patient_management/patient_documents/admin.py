"""
Admin configuration for the Patient Documents module.
"""

from __future__ import annotations

from django.contrib import admin

from .models import PatientDocument


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    """
    Admin configuration for PatientDocument.
    """

    list_display = (
        "document_number",
        "title",
        "patient",
        "category",
        "status",
        "visibility",
        "current_version",
        "created_at",
    )

    list_filter = (
        "category",
        "status",
        "visibility",
        "storage_backend",
        "created_at",
    )

    search_fields = (
        "document_number",
        "title",
        "patient__patient_number",
        "patient__first_name",
        "patient__last_name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "current_version",
    )

    autocomplete_fields = (
        "organization",
        "patient",
    )

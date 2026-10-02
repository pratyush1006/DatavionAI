"""Django admin configuration for Patient Documents."""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.patient_documents.models import (
    PatientDocument,
    PatientDocumentAccessLog,
    PatientDocumentVersion,
)


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    """Admin configuration for patient documents."""

    list_display = (
        "title",
        "patient",
        "organization",
        "category",
        "status",
        "is_confidential",
        "created_at",
    )
    list_filter = (
        "category",
        "status",
        "is_confidential",
        "is_deleted",
    )
    search_fields = (
        "title",
        "original_filename",
        "checksum",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "uploaded_at",
        "archived_at",
    )


@admin.register(PatientDocumentVersion)
class PatientDocumentVersionAdmin(admin.ModelAdmin):
    """Admin configuration for document versions."""

    list_display = (
        "patient_document",
        "version_number",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "patient_document__title",
        "checksum",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(PatientDocumentAccessLog)
class PatientDocumentAccessLogAdmin(admin.ModelAdmin):
    """Admin configuration for document access audit records."""

    list_display = (
        "patient_document",
        "user",
        "action",
        "accessed_at",
    )
    list_filter = ("action",)
    search_fields = (
        "patient_document__title",
        "user__email",
    )
    readonly_fields = (
        "id",
        "accessed_at",
        "created_at",
        "updated_at",
    )


__all__ = (
    "PatientDocumentAccessLogAdmin",
    "PatientDocumentAdmin",
    "PatientDocumentVersionAdmin",
)

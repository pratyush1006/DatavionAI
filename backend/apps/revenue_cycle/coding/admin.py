from __future__ import annotations

"""Django admin configuration for Revenue Cycle Coding."""

from django.contrib import admin

from .models import CodeAssignment, CodingRecord


@admin.register(CodingRecord)
class CodingRecordAdmin(admin.ModelAdmin):
    """Configure CodingRecord administration."""

    list_display = (
        "id",
        "organization",
        "patient",
        "coding_type",
        "status",
        "service_date",
        "is_deleted",
    )
    list_filter = (
        "coding_type",
        "status",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "source_reference",
        "encounter_type",
        "clinical_summary",
        "coding_notes",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )


@admin.register(CodeAssignment)
class CodeAssignmentAdmin(admin.ModelAdmin):
    """Configure CodeAssignment administration."""

    list_display = (
        "id",
        "coding_record",
        "code_system",
        "code",
        "sequence",
        "is_primary",
        "is_deleted",
    )
    list_filter = (
        "code_system",
        "is_primary",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "code",
        "description",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )


__all__ = (
    "CodeAssignmentAdmin",
    "CodingRecordAdmin",
)

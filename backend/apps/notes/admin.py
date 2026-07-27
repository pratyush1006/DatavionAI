"""
Admin configuration for the Notes application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.notes.models import ClinicalNote, NoteTemplate


@admin.register(NoteTemplate)
class NoteTemplateAdmin(admin.ModelAdmin):
    """
    Django admin configuration for NoteTemplate.
    """

    list_display = (
        "name",
        "organization",
        "template_type",
        "is_active",
        "is_system_template",
        "created_at",
    )

    search_fields = (
        "name",
        "template_type",
    )

    list_filter = (
        "organization",
        "template_type",
        "is_active",
        "is_system_template",
        "created_at",
    )

    ordering = ("name",)

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
            "Template Information",
            {
                "fields": (
                    "organization",
                    "name",
                    "template_type",
                ),
            },
        ),
        (
            "Content",
            {
                "fields": ("content",),
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "is_system_template",
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


@admin.register(ClinicalNote)
class ClinicalNoteAdmin(admin.ModelAdmin):
    """
    Django admin configuration for ClinicalNote.
    """

    list_display = (
        "title",
        "organization",
        "patient",
        "note_type",
        "is_amended",
        "signed_at",
        "created_by",
        "created_at",
    )

    search_fields = (
        "title",
        "raw_text",
        "content",
    )

    list_filter = (
        "organization",
        "note_type",
        "is_amended",
        "signed_at",
        "created_by",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "encounter",
        "signed_by",
        "created_by",
        "original_note",
    )

    list_select_related = (
        "organization",
        "patient",
        "encounter",
        "signed_by",
        "created_by",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Note Information",
            {
                "fields": (
                    "organization",
                    "patient",
                    "encounter",
                    "note_type",
                    "title",
                ),
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "content",
                    "raw_text",
                ),
            },
        ),
        (
            "Signing",
            {
                "fields": (
                    "signed_at",
                    "signed_by",
                ),
            },
        ),
        (
            "Amendment",
            {
                "fields": (
                    "is_amended",
                    "amendment_reason",
                    "original_note",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "created_by",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


__all__ = [
    "ClinicalNoteAdmin",
    "NoteTemplateAdmin",
]

"""
Django admin registrations for clinical transcription.
"""

from __future__ import annotations

from django.contrib import admin

from apps.transcription.models import GeneratedNote, TranscriptionJob


@admin.register(TranscriptionJob)
class TranscriptionJobAdmin(admin.ModelAdmin):
    list_display = (
        "job_id",
        "organization",
        "patient",
        "status",
        "provider",
        "created_at",
    )
    list_filter = ("status", "provider", "source_type")
    search_fields = ("job_id", "idempotency_key")
    readonly_fields = (
        "job_id",
        "requested_at",
        "started_at",
        "completed_at",
        "failed_at",
    )


@admin.register(GeneratedNote)
class GeneratedNoteAdmin(admin.ModelAdmin):
    list_display = (
        "note_id",
        "organization",
        "patient",
        "status",
        "note_type",
        "created_at",
    )
    list_filter = ("status", "note_type")
    search_fields = ("note_id",)
    readonly_fields = (
        "note_id",
        "reviewed_at",
        "signed_at",
    )

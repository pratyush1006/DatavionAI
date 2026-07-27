"""
Admin configuration for the Telemedicine application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.telemedicine.models import (
    Participant,
    Recording,
    TelemedicineSession,
)


@admin.register(TelemedicineSession)
class TelemedicineSessionAdmin(admin.ModelAdmin):
    """
    Django admin configuration for TelemedicineSession.
    """

    list_display = (
        "session_id",
        "patient",
        "provider",
        "status",
        "session_type",
        "scheduled_start",
        "scheduled_end",
        "actual_start",
        "actual_end",
        "recording_consent",
        "created_at",
    )

    search_fields = (
        "session_id",
        "patient__first_name",
        "patient__last_name",
        "provider__employee__user__first_name",
        "provider__employee__user__last_name",
        "notes",
    )

    list_filter = (
        "organization",
        "status",
        "session_type",
        "recording_consent",
        "scheduled_start",
        "created_at",
    )

    ordering = ("-scheduled_start",)

    readonly_fields = (
        "id",
        "session_id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "provider",
        "appointment",
    )

    list_select_related = (
        "organization",
        "patient",
        "provider",
        "appointment",
    )

    list_per_page = 25

    date_hierarchy = "scheduled_start"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Session Information",
            {
                "fields": (
                    "organization",
                    "session_id",
                    "patient",
                    "provider",
                    "appointment",
                ),
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "scheduled_start",
                    "scheduled_end",
                    "actual_start",
                    "actual_end",
                ),
            },
        ),
        (
            "Configuration",
            {
                "fields": (
                    "status",
                    "session_type",
                    "recording_consent",
                ),
            },
        ),
        (
            "Connection",
            {
                "fields": (
                    "connection_url",
                    "connection_id",
                    "recording_url",
                ),
            },
        ),
        (
            "Notes",
            {
                "fields": ("notes",),
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


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Participant.
    """

    list_display = (
        "session",
        "user",
        "participant_type",
        "is_present",
        "joined_at",
        "left_at",
        "connection_quality",
        "created_at",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "session__session_id",
        "participant_type",
    )

    list_filter = (
        "session__organization",
        "participant_type",
        "is_present",
        "connection_quality",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "session",
        "user",
    )

    list_select_related = (
        "session",
        "user",
    )

    list_per_page = 25

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Participant Information",
            {
                "fields": (
                    "session",
                    "user",
                    "participant_type",
                ),
            },
        ),
        (
            "Presence",
            {
                "fields": (
                    "is_present",
                    "joined_at",
                    "left_at",
                    "connection_quality",
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


@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Recording.
    """

    list_display = (
        "session",
        "duration_seconds",
        "file_size_bytes",
        "is_processed",
        "created_at",
    )

    search_fields = (
        "session__session_id",
        "recording_url",
        "transcript_text",
    )

    list_filter = (
        "session__organization",
        "is_processed",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("session",)

    list_select_related = ("session",)

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Recording Information",
            {
                "fields": (
                    "session",
                    "recording_url",
                ),
            },
        ),
        (
            "File Details",
            {
                "fields": (
                    "duration_seconds",
                    "file_size_bytes",
                ),
            },
        ),
        (
            "Transcript",
            {
                "fields": (
                    "transcript_url",
                    "transcript_text",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": ("is_processed",),
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


__all__ = [
    "ParticipantAdmin",
    "RecordingAdmin",
    "TelemedicineSessionAdmin",
]

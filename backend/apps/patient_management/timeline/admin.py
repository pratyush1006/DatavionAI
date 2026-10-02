"""
Administrative configuration for Patient Timeline.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.timeline.models.timeline import TimelineEntry


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    """Configure the TimelineEntry admin interface."""

    list_display = (
        "id",
        "patient",
        "event_type",
        "occurred_at",
        "status",
        "is_active",
        "is_active",
        "is_deleted",
        "deleted_by_id",
    )
    list_filter = (
        "event_type",
        "status",
        "is_active",
        "is_deleted",
        "deleted_by_id",
    )
    search_fields = (
        "patient__mrn",
        "title",
        "description",
    )


__all__ = ("TimelineEntryAdmin",)

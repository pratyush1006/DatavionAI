from django.contrib import admin

from apps.telemedicine.models import Participant, Recording, TelemedicineSession


@admin.register(TelemedicineSession)
class TelemedicineSessionAdmin(admin.ModelAdmin):
    list_display = (
        "session_id",
        "organization",
        "patient",
        "provider",
        "status",
        "scheduled_start",
        "scheduled_end",
    )
    list_filter = ("status", "session_type", "recording_consent")
    search_fields = ("session_id", "connection_id")
    readonly_fields = ("session_id", "actual_start", "actual_end")


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "user",
        "participant_type",
        "status",
        "joined_at",
        "left_at",
    )
    list_filter = ("participant_type", "status")


@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ("recording_id", "session", "status", "started_at", "finalized_at")
    list_filter = ("status",)
    search_fields = ("recording_id",)

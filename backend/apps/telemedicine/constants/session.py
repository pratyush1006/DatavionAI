from django.db import models


class SessionStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SCHEDULED = "scheduled", "Scheduled"
    CONFIRMED = "confirmed", "Confirmed"
    READY = "ready", "Ready"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    NO_SHOW = "no_show", "No Show"
    FAILED = "failed", "Failed"


class SessionType(models.TextChoices):
    VIDEO = "video", "Video"
    AUDIO = "audio", "Audio"
    CHAT = "chat", "Chat"


DEFAULT_SESSION_STATUS = SessionStatus.SCHEDULED

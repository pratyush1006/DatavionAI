"""Live transcription state and source constants."""

from django.db import models


class LiveSessionStatus(models.TextChoices):
    CREATED = "created", "Created"
    READY = "ready", "Ready"
    CONNECTING = "connecting", "Connecting"
    RECORDING = "recording", "Recording"
    PAUSED = "paused", "Paused"
    RECONNECTING = "reconnecting", "Reconnecting"
    FINALIZING = "finalizing", "Finalizing"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


class LiveSegmentKind(models.TextChoices):
    PARTIAL = "partial", "Partial"
    FINAL = "final", "Final"


class LiveSource(models.TextChoices):
    BROWSER = "browser", "Browser"
    DEVICE_PLATFORM = "device_platform", "Device Platform"
    TELEMEDICINE = "telemedicine", "Telemedicine"
    DICTATION = "dictation", "Dictation"

from django.db import models


class RecordingStatus(models.TextChoices):
    REQUESTED = "requested", "Requested"
    RECORDING = "recording", "Recording"
    FINALIZING = "finalizing", "Finalizing"
    READY = "ready", "Ready"
    FAILED = "failed", "Failed"

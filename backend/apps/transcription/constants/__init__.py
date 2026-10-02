"""
Transcription domain constants.
"""

from __future__ import annotations

from django.db import models


class TranscriptionStatus(models.TextChoices):
    CREATED = "created", "Created"
    QUEUED = "queued", "Queued"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


class NoteStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    REVIEW = "review", "Review"
    SIGNED = "signed", "Signed"
    REJECTED = "rejected", "Rejected"


class SourceType(models.TextChoices):
    UPLOAD = "upload", "Upload"
    LIVE = "live", "Live Recording"
    TELEMEDICINE = "telemedicine", "Telemedicine"
    DICTATION = "dictation", "Dictation"
    EXTERNAL = "external", "External"


class TranscriptionProvider(models.TextChoices):
    OPENAI_WHISPER = "openai_whisper", "OpenAI Whisper"
    AZURE_SPEECH = "azure_speech", "Azure Speech"
    GOOGLE_SPEECH = "google_speech", "Google Speech"
    AWS_TRANSCRIBE = "aws_transcribe", "AWS Transcribe"
    CUSTOM = "custom", "Custom"

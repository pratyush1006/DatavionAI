"""
URL configuration for clinical transcription APIs.
"""

from __future__ import annotations

from apps.transcription.api.views import (
    GeneratedNoteDetailAPIView,
    GeneratedNoteGenerateAPIView,
    GeneratedNoteReviewAPIView,
    GeneratedNoteSignAPIView,
    LiveSessionNoteGenerateAPIView,
    LiveTranscriptionTicketAPIView,
    TranscriptionJobActionAPIView,
    TranscriptionJobDetailAPIView,
    TranscriptionJobListCreateAPIView,
)
from django.urls import path

urlpatterns = [
    path(
        "live-sessions/<uuid:session_id>/notes/generate/",
        LiveSessionNoteGenerateAPIView.as_view(),
        name="transcription-live-session-note-generate",
    ),
    path(
        "live-sessions/<uuid:session_id>/ticket/",
        LiveTranscriptionTicketAPIView.as_view(),
        name="transcription-live-session-ticket",
    ),
    path(
        "jobs/",
        TranscriptionJobListCreateAPIView.as_view(),
        name="transcription-job-list-create",
    ),
    path(
        "jobs/<uuid:job_id>/",
        TranscriptionJobDetailAPIView.as_view(),
        name="transcription-job-detail",
    ),
    path(
        "jobs/<uuid:job_id>/<str:action>/",
        TranscriptionJobActionAPIView.as_view(),
        name="transcription-job-action",
    ),
    path(
        "jobs/<uuid:job_id>/notes/generate/",
        GeneratedNoteGenerateAPIView.as_view(),
        name="transcription-note-generate",
    ),
    path(
        "notes/<uuid:note_id>/",
        GeneratedNoteDetailAPIView.as_view(),
        name="transcription-note-detail",
    ),
    path(
        "notes/<uuid:note_id>/review/",
        GeneratedNoteReviewAPIView.as_view(),
        name="transcription-note-review",
    ),
    path(
        "notes/<uuid:note_id>/sign/",
        GeneratedNoteSignAPIView.as_view(),
        name="transcription-note-sign",
    ),
]

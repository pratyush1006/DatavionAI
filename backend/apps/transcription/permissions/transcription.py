"""
Permission declarations for clinical transcription.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class TranscriptionPermission:
    VIEW = "transcription.view"
    CREATE = "transcription.create"
    RUN = "transcription.run"
    CANCEL = "transcription.cancel"
    GENERATE_NOTE = "transcription.note.generate"
    REVIEW_NOTE = "transcription.note.review"
    SIGN_NOTE = "transcription.note.sign"


class CanViewTranscription(BasePermission):
    permission_code = TranscriptionPermission.VIEW


class CanCreateTranscription(BasePermission):
    permission_code = TranscriptionPermission.CREATE


class CanRunTranscription(BasePermission):
    permission_code = TranscriptionPermission.RUN


class CanCancelTranscription(BasePermission):
    permission_code = TranscriptionPermission.CANCEL


class CanGenerateNote(BasePermission):
    permission_code = TranscriptionPermission.GENERATE_NOTE


class CanReviewNote(BasePermission):
    permission_code = TranscriptionPermission.REVIEW_NOTE


class CanSignNote(BasePermission):
    permission_code = TranscriptionPermission.SIGN_NOTE

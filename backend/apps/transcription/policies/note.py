"""
Business policies for generated clinical notes.
"""

from __future__ import annotations

from apps.transcription.constants import NoteStatus
from apps.transcription.rbac import has_permission


class GeneratedNotePolicy:
    @staticmethod
    def can_view(*, actor, note) -> bool:
        return bool(
            actor
            and actor.is_authenticated
            and note.organization_id == getattr(actor, "organization_id", None)
            and has_permission(
                user=actor,
                organization=note.organization,
                permission="transcription.view",
            )
        )

    @staticmethod
    def can_review(*, actor, note) -> bool:
        return (
            GeneratedNotePolicy.can_view(actor=actor, note=note)
            and has_permission(
                user=actor,
                organization=note.organization,
                permission="transcription.note.review",
            )
            and note.status
            in {
                NoteStatus.DRAFT,
                NoteStatus.REVIEW,
            }
        )

    @staticmethod
    def can_sign(*, actor, note) -> bool:
        return (
            GeneratedNotePolicy.can_view(actor=actor, note=note)
            and has_permission(
                user=actor,
                organization=note.organization,
                permission="transcription.note.sign",
            )
            and note.status == NoteStatus.REVIEW
        )

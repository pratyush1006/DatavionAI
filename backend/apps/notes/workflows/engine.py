from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.notes.models import ClinicalNote, NoteTransition


class ClinicalNoteWorkflow:
    GRAPH = {
        "draft": {"in_review", "cancelled"},
        "in_review": {"draft", "signed", "cancelled"},
        "signed": {"amended"},
        "amended": {"signed"},
        "cancelled": set(),
    }

    @classmethod
    @transaction.atomic
    def transition(
        cls, *, note_id, organization_id, actor, target, reason="", correlation_id=""
    ):
        note = (
            ClinicalNote.objects.select_for_update()
            .select_related("organization")
            .get(note_id=note_id, organization_id=organization_id)
        )
        if target not in cls.GRAPH.get(note.status, set()):
            raise ValueError(
                f"Invalid Clinical Note transition: {note.status} -> {target}"
            )
        previous = note.status
        note.status = target
        if target == "signed":
            note.signed_by = actor
            note.signed_at = note.signed_at or timezone.now()
            note.locked_at = timezone.now()
        elif target == "amended":
            note.locked_at = None
        note.version += 1
        note.save(
            update_fields=(
                "status",
                "signed_by",
                "signed_at",
                "locked_at",
                "version",
                "updated_at",
            )
        )
        NoteTransition.objects.create(
            organization=note.organization,
            note=note,
            from_status=previous,
            to_status=target,
            actor=actor,
            version=note.version,
            reason=reason,
            correlation_id=correlation_id,
        )
        return note

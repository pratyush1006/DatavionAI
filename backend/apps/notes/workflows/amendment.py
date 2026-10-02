from django.db import transaction

from apps.core.events import publish_after_commit
from apps.notes.events import ClinicalNoteAmendedEvent
from apps.notes.models import ClinicalNote, ClinicalNoteAmendment
from apps.notes.workflows.engine import ClinicalNoteWorkflow


class ClinicalNoteAmendmentService:
    @staticmethod
    @transaction.atomic
    def request(
        *, note, actor, reason, proposed_body, proposed_structured_content=None
    ):
        if note.status not in {"signed", "amended"}:
            raise ValueError("Only signed notes can be amended.")
        amendment = ClinicalNoteAmendment.objects.create(
            organization=note.organization,
            note=note,
            requested_by=actor,
            reason=reason,
            proposed_body=proposed_body,
            proposed_structured_content=proposed_structured_content or {},
        )
        ClinicalNoteWorkflow.transition(
            note_id=note.note_id,
            organization_id=note.organization_id,
            actor=actor,
            target="amended",
            reason=reason,
        )
        publish_after_commit(
            ClinicalNoteAmendedEvent(
                tenant_id=note.organization.tenant_id,
                note_id=note.note_id,
                organization_id=note.organization_id,
                patient_id=note.patient_id,
                amendment_id=amendment.amendment_id,
            )
        )
        return amendment

    @staticmethod
    @transaction.atomic
    def accept(*, amendment, actor):
        amendment.status = "accepted"
        amendment.reviewed_by = actor
        amendment.save(
            update_fields=("status", "reviewed_by", "reviewed_at", "updated_at"),
        )
        note = ClinicalNote.objects.select_for_update().get(pk=amendment.note_id)
        note.body = amendment.proposed_body
        note.structured_content = amendment.proposed_structured_content
        note.version += 1
        note.save(update_fields=("body", "structured_content", "version", "updated_at"))
        return note

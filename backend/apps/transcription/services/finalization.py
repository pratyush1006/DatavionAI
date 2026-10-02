from __future__ import annotations

from django.db import transaction

from apps.transcription.integrations.clinical_notes import ClinicalNotesIntegration
from apps.transcription.integrations.documents import DocumentsIntegration
from apps.transcription.integrations.storage import StorageIntegration
from apps.transcription.services.outbox import enqueue_event


@transaction.atomic
def finalize_signed_note(*, note, actor, transcript_text: str):
    if getattr(note, "status", None) != "signed":
        raise ValueError("Only a signed transcription note may be finalized.")
    note_ref = ClinicalNotesIntegration().attach_transcription(
        note=note, transcript_text=transcript_text, actor=actor
    )
    document_ref = DocumentsIntegration().create_signed_note_reference(
        note=note, actor=actor
    )
    storage_ref = StorageIntegration().create_artifact_reference(
        organization=note.organization,
        artifact_type="signed_clinical_note",
        artifact_id=str(note.pk),
        metadata={"note_reference": note_ref, "document_reference": document_ref},
    )
    transaction.on_commit(
        lambda: enqueue_event(
            organization=note.organization,
            event_type="transcription.note.signed",
            aggregate_type="GeneratedNote",
            aggregate_id=str(note.pk),
            payload={
                "note_id": str(note.pk),
                "document_reference": document_ref,
                "storage_reference": storage_ref,
            },
        )
    )
    return {
        "note_reference": note_ref,
        "document_reference": document_ref,
        "storage_reference": storage_ref,
    }

from __future__ import annotations

from django.db import transaction

from apps.notes.integrations.documents import build_document_reference
from apps.notes.integrations.storage import build_storage_reference
from apps.notes.services.outbox import enqueue_event


@transaction.atomic
def finalize_signed_note(*, note):
    if note.status != "signed":
        raise ValueError("Only signed Clinical Notes can be finalized.")
    document_ref = build_document_reference(note=note)
    storage_ref = build_storage_reference(note=note)
    note.document_reference = document_ref["note_id"]
    note.storage_reference = storage_ref["object_key"]
    note.save(update_fields=("document_reference", "storage_reference", "updated_at"))
    transaction.on_commit(
        lambda: enqueue_event(
            organization=note.organization,
            event_type="notes.note.signed",
            aggregate_type="ClinicalNote",
            aggregate_id=str(note.note_id),
            payload={
                "note_id": str(note.note_id),
                "document_reference": document_ref,
                "storage_reference": storage_ref,
            },
        )
    )
    return note

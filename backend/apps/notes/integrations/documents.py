from __future__ import annotations


def build_document_reference(*, note):
    return {
        "owner": "apps.notes",
        "document_type": "clinical_note",
        "note_id": str(note.note_id),
        "version": note.version,
    }

from __future__ import annotations


def build_storage_reference(*, note):
    return {
        "owner": "external_storage",
        "object_key": f"clinical-notes/{note.organization_id}/{note.note_id}/v{note.version}",
    }

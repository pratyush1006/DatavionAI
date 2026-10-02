"""Storage integration; Transcription stores external references only."""


def build_storage_reference(*, object_key, media_type, session_id):
    return {
        "object_key": object_key,
        "media_type": media_type,
        "session_id": session_id,
        "owner": "external_storage",
    }

from __future__ import annotations

from apps.transcription.models import GeneratedNote


def import_transcription_draft(
    *, organization, patient, encounter, transcription_note_id
):
    generated = GeneratedNote.objects.select_related("job").get(
        note_id=transcription_note_id, organization_id=organization.id
    )
    if generated.patient_id != patient.id:
        raise ValueError("Transcription note belongs to another patient.")
    if generated.encounter_id and encounter and generated.encounter_id != encounter.id:
        raise ValueError("Transcription note belongs to another encounter.")
    return {
        "title": f"Transcription - {generated.note_type}",
        "body": generated.draft_text,
        "structured_content": generated.structured_content,
        "source": "transcription",
        "transcription_job_id": generated.job_id,
    }

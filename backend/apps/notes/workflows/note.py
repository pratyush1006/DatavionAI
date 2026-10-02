from django.db import transaction

from apps.core.events import publish_after_commit
from apps.notes.constants import NoteSource, NoteStatus, NoteType
from apps.notes.events import (
    ClinicalNoteCancelledEvent,
    ClinicalNoteCreatedEvent,
    ClinicalNoteReviewedEvent,
    ClinicalNoteSignedEvent,
)
from apps.notes.models import ClinicalNote, ClinicalNoteVersion
from apps.notes.workflows.engine import ClinicalNoteWorkflow


class ClinicalNoteService:
    @staticmethod
    @transaction.atomic
    def create(
        *,
        organization,
        patient,
        author,
        title,
        body="",
        note_type=NoteType.SOAP,
        encounter=None,
        source=NoteSource.MANUAL,
        structured_content=None,
        metadata=None,
        transcription_job_id=None,
        telemedicine_session_id=None,
    ):
        note = ClinicalNote.objects.create(
            organization=organization,
            patient=patient,
            encounter=encounter,
            author=author,
            title=title,
            body=body,
            note_type=note_type,
            source=source,
            structured_content=structured_content or {},
            metadata=metadata or {},
            transcription_job_id=transcription_job_id,
            telemedicine_session_id=telemedicine_session_id,
        )
        ClinicalNoteVersion.objects.create(
            organization=organization,
            note=note,
            version_number=1,
            title=title,
            body=body,
            structured_content=structured_content or {},
            changed_by=author,
            change_reason="Initial version",
        )
        publish_after_commit(
            ClinicalNoteCreatedEvent(
                tenant_id=organization.tenant_id,
                note_id=note.note_id,
                organization_id=organization.id,
                patient_id=patient.id,
                encounter_id=getattr(encounter, "id", None),
            )
        )
        return note

    @staticmethod
    @transaction.atomic
    def update_draft(
        *,
        note_id,
        organization_id,
        actor,
        title=None,
        body=None,
        structured_content=None,
        reason="",
    ):
        note = ClinicalNote.objects.select_for_update().get(
            note_id=note_id, organization_id=organization_id
        )
        if note.status not in {NoteStatus.DRAFT, NoteStatus.IN_REVIEW}:
            raise ValueError(
                "Signed Clinical Notes cannot be edited directly; create an amendment."
            )
        if title is not None:
            note.title = title
        if body is not None:
            note.body = body
        if structured_content is not None:
            note.structured_content = structured_content
        note.version += 1
        note.save(
            update_fields=(
                "title",
                "body",
                "structured_content",
                "version",
                "updated_at",
            )
        )
        ClinicalNoteVersion.objects.create(
            organization=note.organization,
            note=note,
            version_number=note.version,
            title=note.title,
            body=note.body,
            structured_content=note.structured_content,
            changed_by=actor,
            change_reason=reason or "Clinical Note edit",
        )
        return note

    @staticmethod
    def submit_for_review(*, note_id, organization_id, actor):
        note = ClinicalNoteWorkflow.transition(
            note_id=note_id,
            organization_id=organization_id,
            actor=actor,
            target=NoteStatus.IN_REVIEW,
        )
        publish_after_commit(
            ClinicalNoteReviewedEvent(
                tenant_id=note.organization.tenant_id,
                note_id=note.note_id,
                organization_id=note.organization_id,
                patient_id=note.patient_id,
            )
        )
        return note

    @staticmethod
    def sign(*, note_id, organization_id, actor):
        note = ClinicalNoteWorkflow.transition(
            note_id=note_id,
            organization_id=organization_id,
            actor=actor,
            target=NoteStatus.SIGNED,
            reason="Clinical Note signed",
        )
        publish_after_commit(
            ClinicalNoteSignedEvent(
                tenant_id=note.organization.tenant_id,
                note_id=note.note_id,
                organization_id=note.organization_id,
                patient_id=note.patient_id,
            )
        )
        return note

    @staticmethod
    def cancel(*, note_id, organization_id, actor, reason=""):
        note = ClinicalNoteWorkflow.transition(
            note_id=note_id,
            organization_id=organization_id,
            actor=actor,
            target=NoteStatus.CANCELLED,
            reason=reason,
        )
        publish_after_commit(
            ClinicalNoteCancelledEvent(
                tenant_id=note.organization.tenant_id,
                note_id=note.note_id,
                organization_id=note.organization_id,
                patient_id=note.patient_id,
            )
        )
        return note

"""
Application services for clinical transcription.
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.core.events import publish_after_commit
from apps.transcription.constants import (
    NoteStatus,
    SourceType,
    TranscriptionProvider,
    TranscriptionStatus,
)
from apps.transcription.events import (
    ClinicalNoteGeneratedEvent,
    ClinicalNoteReviewedEvent,
    ClinicalNoteSignedEvent,
    TranscriptionCompletedEvent,
    TranscriptionCreatedEvent,
    TranscriptionFailedEvent,
    TranscriptionStartedEvent,
)
from apps.transcription.integrations import get_note_generator, get_speech_provider
from apps.transcription.models import (
    GeneratedNote,
    LiveTranscriptionSession,
    TranscriptionJob,
)


class TranscriptionService:
    @staticmethod
    @transaction.atomic
    def create_completed_live_job(*, session_id, organization_id) -> TranscriptionJob:
        """Persist the final transcript as a completed, idempotent transcription job."""

        session = (
            LiveTranscriptionSession.objects.select_for_update()
            .select_related(
                "organization",
                "patient",
                "created_by",
                "encounter",
            )
            .get(
                session_id=session_id,
                organization_id=organization_id,
            )
        )
        if session.status != "completed":
            raise ValueError("The live session must be stopped before note generation.")

        segments = list(session.segments.filter(is_current=True).order_by("sequence"))
        final_segments = [segment for segment in segments if segment.kind == "final"]
        selected = final_segments or segments
        transcript = " ".join(
            segment.text.strip() for segment in selected if segment.text.strip()
        )
        if not transcript:
            raise ValueError(
                "The live session contains no transcript to generate a note from."
            )

        job, _ = TranscriptionJob.objects.get_or_create(
            organization=session.organization,
            idempotency_key=f"live-session:{session.session_id}",
            defaults={
                "patient": session.patient,
                "encounter": session.encounter,
                "created_by": session.created_by,
                "source_type": SourceType.LIVE,
                "provider": TranscriptionProvider.CUSTOM,
                "status": TranscriptionStatus.COMPLETED,
                "audio_uri": "",
                "audio_mime_type": session.audio_mime_type,
                "language": session.language,
                "started_at": session.started_at,
                "completed_at": session.ended_at or timezone.now(),
                "transcript_text": transcript,
                "transcript_json": {
                    "segments": [
                        {
                            "sequence": segment.sequence,
                            "text": segment.text,
                            "speaker": segment.speaker_label,
                            "start_ms": segment.start_ms,
                            "end_ms": segment.end_ms,
                        }
                        for segment in selected
                    ],
                    "live_session_id": str(session.session_id),
                },
                "metadata": {"live_session_id": str(session.session_id)},
            },
        )
        return job

    @staticmethod
    @transaction.atomic
    def create_job(
        *,
        organization,
        patient,
        created_by,
        audio_uri: str,
        idempotency_key: str,
        encounter=None,
        source_type: str = "upload",
        provider: str = "openai_whisper",
        language: str = "en",
        audio_mime_type: str = "",
        metadata: dict | None = None,
    ) -> TranscriptionJob:
        job, created = TranscriptionJob.objects.select_for_update().get_or_create(
            organization=organization,
            idempotency_key=idempotency_key,
            defaults={
                "patient": patient,
                "created_by": created_by,
                "encounter": encounter,
                "audio_uri": audio_uri,
                "source_type": source_type,
                "provider": provider,
                "language": language,
                "audio_mime_type": audio_mime_type,
                "metadata": metadata or {},
            },
        )
        if not created:
            return job

        publish_after_commit(
            TranscriptionCreatedEvent(
                tenant_id=organization.tenant_id,
                job_id=job.job_id,
                organization_id=organization.id,
                patient_id=patient.id,
            )
        )
        return job

    @staticmethod
    @transaction.atomic
    def queue(*, job_id, organization_id) -> TranscriptionJob:
        job = (
            TranscriptionJob.objects.select_for_update()
            .select_related("organization")
            .get(
                job_id=job_id,
                organization_id=organization_id,
            )
        )
        if job.status not in {
            TranscriptionStatus.CREATED,
            TranscriptionStatus.QUEUED,
        }:
            raise ValueError("Only created or queued transcription jobs can be queued.")

        job.status = TranscriptionStatus.QUEUED
        job.save(update_fields=["status", "updated_at"])
        return job

    @staticmethod
    @transaction.atomic
    def run(*, job_id, organization_id) -> TranscriptionJob:
        job = (
            TranscriptionJob.objects.select_for_update()
            .select_related("organization")
            .get(
                job_id=job_id,
                organization_id=organization_id,
            )
        )

        if job.status not in {
            TranscriptionStatus.CREATED,
            TranscriptionStatus.QUEUED,
        }:
            if job.status == TranscriptionStatus.COMPLETED:
                return job
            raise ValueError("Only created or queued jobs can be processed.")

        now = timezone.now()
        job.status = TranscriptionStatus.PROCESSING
        job.started_at = now
        job.failed_at = None
        job.error_code = ""
        job.error_message = ""
        job.save(
            update_fields=(
                "status",
                "started_at",
                "failed_at",
                "error_code",
                "error_message",
                "updated_at",
            )
        )

        publish_after_commit(
            TranscriptionStartedEvent(
                tenant_id=job.organization.tenant_id,
                job_id=job.job_id,
                organization_id=job.organization_id,
                patient_id=job.patient_id,
            )
        )

        try:
            result = get_speech_provider().transcribe(
                audio_uri=job.audio_uri,
                language=job.language,
                mime_type=job.audio_mime_type,
            )
        except Exception as exc:
            locked = TranscriptionJob.objects.select_for_update().get(pk=job.pk)
            locked.status = TranscriptionStatus.FAILED
            locked.failed_at = timezone.now()
            locked.error_code = exc.__class__.__name__
            locked.error_message = str(exc)
            locked.save(
                update_fields=(
                    "status",
                    "failed_at",
                    "error_code",
                    "error_message",
                    "updated_at",
                )
            )
            publish_after_commit(
                TranscriptionFailedEvent(
                    tenant_id=locked.organization.tenant_id,
                    job_id=locked.job_id,
                    organization_id=locked.organization_id,
                    patient_id=locked.patient_id,
                    error_code=locked.error_code,
                )
            )
            return locked

        locked = TranscriptionJob.objects.select_for_update().get(pk=job.pk)
        locked.status = TranscriptionStatus.COMPLETED
        locked.completed_at = timezone.now()
        locked.transcript_text = result.text
        locked.transcript_json = {
            "segments": result.segments,
            "provider": result.provider,
        }
        locked.language = result.language or locked.language
        locked.duration_seconds = result.duration_seconds
        locked.speaker_count = result.speaker_count
        locked.provider = result.provider or locked.provider
        locked.save(
            update_fields=(
                "status",
                "completed_at",
                "transcript_text",
                "transcript_json",
                "language",
                "duration_seconds",
                "speaker_count",
                "provider",
                "updated_at",
            )
        )

        publish_after_commit(
            TranscriptionCompletedEvent(
                tenant_id=locked.organization.tenant_id,
                job_id=locked.job_id,
                organization_id=locked.organization_id,
                patient_id=locked.patient_id,
            )
        )
        return locked

    @staticmethod
    @transaction.atomic
    def cancel(*, job_id, organization_id) -> TranscriptionJob:
        job = (
            TranscriptionJob.objects.select_for_update()
            .select_related("organization")
            .get(
                job_id=job_id,
                organization_id=organization_id,
            )
        )
        if job.status in {
            TranscriptionStatus.COMPLETED,
            TranscriptionStatus.CANCELLED,
            TranscriptionStatus.FAILED,
        }:
            return job
        job.status = TranscriptionStatus.CANCELLED
        job.save(update_fields=["status", "updated_at"])
        return job

    @staticmethod
    @transaction.atomic
    def generate_note(
        *,
        job_id,
        organization_id,
        note_type: str = "soap",
    ) -> GeneratedNote:
        job = (
            TranscriptionJob.objects.select_for_update()
            .select_related("organization")
            .get(
                job_id=job_id,
                organization_id=organization_id,
            )
        )
        if job.status != TranscriptionStatus.COMPLETED:
            raise ValueError(
                "A clinical note can only be generated from a completed transcription."
            )

        existing = GeneratedNote.objects.filter(job=job).first()
        if existing:
            return existing

        generated = get_note_generator().generate(
            transcript=job.transcript_text,
            patient_id=str(job.patient_id),
            encounter_id=str(job.encounter_id) if job.encounter_id else None,
            note_type=note_type,
        )

        note = GeneratedNote.objects.create(
            organization=job.organization,
            job=job,
            patient=job.patient,
            encounter=job.encounter,
            note_type=note_type,
            draft_text=generated["draft_text"],
            structured_content=generated.get("structured_content", {}),
            generated_by_provider=generated.get("provider", ""),
        )
        publish_after_commit(
            ClinicalNoteGeneratedEvent(
                tenant_id=job.organization.tenant_id,
                note_id=note.note_id,
                organization_id=note.organization_id,
                patient_id=note.patient_id,
            )
        )
        return note

    @staticmethod
    @transaction.atomic
    def review_note(
        *,
        note_id,
        organization_id,
        reviewer,
        decision: str,
        rejection_reason: str = "",
    ) -> GeneratedNote:
        note = (
            GeneratedNote.objects.select_for_update()
            .select_related("organization")
            .get(
                note_id=note_id,
                organization_id=organization_id,
            )
        )

        if decision == "approve":
            note.status = NoteStatus.REVIEW
            note.reviewed_by = reviewer
            note.reviewed_at = timezone.now()
            note.rejection_reason = ""
        elif decision == "reject":
            note.status = NoteStatus.REJECTED
            note.reviewed_by = reviewer
            note.reviewed_at = timezone.now()
            note.rejection_reason = rejection_reason.strip()
            if not note.rejection_reason:
                raise ValueError("A rejection reason is required.")
        else:
            raise ValueError("Decision must be approve or reject.")

        note.save(
            update_fields=(
                "status",
                "reviewed_by",
                "reviewed_at",
                "rejection_reason",
                "updated_at",
            )
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
    @transaction.atomic
    def update_note_draft(
        *, note_id, organization_id, editor, draft_text
    ) -> GeneratedNote:
        """Save clinician edits while a generated note remains unsigned."""

        note = GeneratedNote.objects.select_for_update().get(
            note_id=note_id,
            organization_id=organization_id,
        )
        if note.status not in {NoteStatus.DRAFT, NoteStatus.REJECTED}:
            raise ValueError("Only an unapproved note draft can be edited.")
        cleaned = draft_text.strip()
        if not cleaned:
            raise ValueError("Clinical note text cannot be blank.")
        note.draft_text = cleaned
        note.save(update_fields=("draft_text", "updated_at"))
        return note

    @staticmethod
    @transaction.atomic
    def sign_note(*, note_id, organization_id, signer) -> GeneratedNote:
        note = (
            GeneratedNote.objects.select_for_update()
            .select_related("organization")
            .get(
                note_id=note_id,
                organization_id=organization_id,
            )
        )
        if note.status != NoteStatus.REVIEW:
            raise ValueError("Only reviewed notes can be signed.")

        note.status = NoteStatus.SIGNED
        note.signed_at = timezone.now()
        note.save(update_fields=("status", "signed_at", "updated_at"))

        publish_after_commit(
            ClinicalNoteSignedEvent(
                tenant_id=note.organization.tenant_id,
                note_id=note.note_id,
                organization_id=note.organization_id,
                patient_id=note.patient_id,
            )
        )
        return note


__all__ = ("TranscriptionService",)

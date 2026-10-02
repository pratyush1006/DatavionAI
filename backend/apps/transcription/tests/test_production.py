"""
Production-contract tests for clinical transcription.
"""

from __future__ import annotations

from datetime import date
from unittest.mock import patch

from django.apps import apps
from django.test import TestCase

from apps.core.workflows import WorkflowContext
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.transcription.constants import NoteStatus, TranscriptionStatus
from apps.transcription.integrations.providers import TranscriptionResult
from apps.transcription.models import GeneratedNote, TranscriptionJob
from apps.transcription.services import TranscriptionService
from apps.transcription.workflows import (
    ClinicalNoteGenerateWorkflow,
    ClinicalNoteReviewWorkflow,
    ClinicalNoteSignWorkflow,
    TranscriptionJobCreateWorkflow,
    TranscriptionJobRunWorkflow,
)


class FakeSpeechProvider:
    def transcribe(self, *, audio_uri, language, mime_type):
        return TranscriptionResult(
            text="Patient reports cough and fever for three days.",
            segments=[{"start": 0, "end": 2, "text": "Patient reports cough."}],
            language=language,
            duration_seconds=42,
            speaker_count=2,
            provider="fake_speech",
        )


class FakeNoteProvider:
    def generate(self, *, transcript, patient_id, encounter_id, note_type):
        return {
            "draft_text": "S: Cough and fever for three days.\nO: Not provided.\nA: Acute respiratory symptoms.\nP: Clinical evaluation recommended.",
            "structured_content": {
                "subjective": transcript,
                "objective": "",
                "assessment": "Acute respiratory symptoms.",
                "plan": "Clinical evaluation recommended.",
            },
            "provider": "fake_note",
        }


class TranscriptionProductionTests(TestCase):
    def setUp(self):
        Tenant = apps.get_model("tenancy", "Tenant")
        Patient = apps.get_model("patient_core", "Patient")
        self.tenant = Tenant.objects.create(
            name="Transcription Test Tenant",
            slug="transcription-test-tenant",
        )
        self.organization = Organization.objects.create(
            tenant=self.tenant,
            name="Transcription Test Org",
            code="TRANSCRIPTION-TEST",
            slug="transcription-test-org",
        )
        self.user = User.objects.create(
            email="transcription@example.com",
            username="transcription@example.com",
        )
        self.user.organization = self.organization
        self.user.save(update_fields=["organization"])
        self.patient = Patient.objects.create(
            organization=self.organization,
            first_name="Test",
            last_name="Patient",
            date_of_birth=date(1985, 1, 15),
        )

    def _context(self, name):
        return WorkflowContext.create(
            tenant_id=self.organization.tenant_id,
            actor_id=self.user.id,
            workflow_name=name,
        )

    @patch(
        "apps.transcription.integrations.providers.get_speech_provider",
        return_value=FakeSpeechProvider(),
    )
    def test_full_transcription_to_signed_note_e2e(self, _speech):
        with (
            patch(
                "apps.transcription.services.get_speech_provider",
                return_value=FakeSpeechProvider(),
            ),
            patch(
                "apps.transcription.services.get_note_generator",
                return_value=FakeNoteProvider(),
            ),
        ):
            create = TranscriptionJobCreateWorkflow(
                payload={
                    "organization": self.organization,
                    "patient": self.patient,
                    "created_by": self.user,
                    "audio_uri": "https://example.com/audio/test.wav",
                    "idempotency_key": "e2e-001",
                    "language": "en",
                    "source_type": "upload",
                    "provider": "openai_whisper",
                    "audio_mime_type": "audio/wav",
                }
            ).execute(context=self._context("transcription.job.create"))
            self.assertTrue(create.success)
            job = create.data

            run = TranscriptionJobRunWorkflow(
                payload={
                    "job_id": job.job_id,
                    "organization_id": self.organization.id,
                }
            ).execute(context=self._context("transcription.job.run"))
            self.assertTrue(run.success)
            job.refresh_from_db()
            self.assertEqual(job.status, TranscriptionStatus.COMPLETED)
            self.assertTrue(job.transcript_text)

            note_result = ClinicalNoteGenerateWorkflow(
                payload={
                    "job_id": job.job_id,
                    "organization_id": self.organization.id,
                    "note_type": "soap",
                }
            ).execute(context=self._context("transcription.note.generate"))
            self.assertTrue(note_result.success)

            note = note_result.data
            self.assertEqual(note.status, NoteStatus.DRAFT)

            reviewed = ClinicalNoteReviewWorkflow(
                payload={
                    "note_id": note.note_id,
                    "organization_id": self.organization.id,
                    "reviewer": self.user,
                    "decision": "approve",
                }
            ).execute(context=self._context("transcription.note.review"))
            self.assertTrue(reviewed.success)

            signed = ClinicalNoteSignWorkflow(
                payload={
                    "note_id": note.note_id,
                    "organization_id": self.organization.id,
                    "signer": self.user,
                }
            ).execute(context=self._context("transcription.note.sign"))
            self.assertTrue(signed.success)
            note.refresh_from_db()
            self.assertEqual(note.status, NoteStatus.SIGNED)

    @patch(
        "apps.transcription.services.get_speech_provider",
        return_value=FakeSpeechProvider(),
    )
    def test_idempotent_creation_returns_same_job(self, _provider):
        first = TranscriptionService.create_job(
            organization=self.organization,
            patient=self.patient,
            created_by=self.user,
            audio_uri="https://example.com/audio/a.wav",
            idempotency_key="same-key",
        )
        second = TranscriptionService.create_job(
            organization=self.organization,
            patient=self.patient,
            created_by=self.user,
            audio_uri="https://example.com/audio/other.wav",
            idempotency_key="same-key",
        )
        self.assertEqual(first.id, second.id)

    def test_tenant_scope_is_enforced(self):
        other_org = Organization.objects.create(
            tenant=self.tenant,
            name="Other Org",
            code="OTHER-TRANSCRIPTION",
            slug="other-transcription-org",
        )
        TranscriptionJob.objects.create(
            organization=self.organization,
            patient=self.patient,
            created_by=self.user,
            audio_uri="https://example.com/audio/a.wav",
            idempotency_key="scope-key",
        )
        self.assertEqual(
            TranscriptionJob.objects.filter(
                organization=other_org,
            ).count(),
            0,
        )

    def test_note_sign_requires_review(self):
        job = TranscriptionJob.objects.create(
            organization=self.organization,
            patient=self.patient,
            created_by=self.user,
            audio_uri="https://example.com/audio/a.wav",
            idempotency_key="note-sign-key",
            status=TranscriptionStatus.COMPLETED,
            transcript_text="Transcript",
        )
        note = GeneratedNote.objects.create(
            organization=self.organization,
            job=job,
            patient=self.patient,
            draft_text="Draft",
        )
        with self.assertRaises(ValueError):
            TranscriptionService.sign_note(
                note_id=note.note_id,
                organization_id=self.organization.id,
                signer=self.user,
            )

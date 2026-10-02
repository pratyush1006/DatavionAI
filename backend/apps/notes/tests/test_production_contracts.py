from pathlib import Path

from django.test import SimpleTestCase


class NotesProductionContractTests(SimpleTestCase):
    root = Path(__file__).resolve().parents[1]

    def test_integration_boundaries(self):
        for name in (
            "transcription.py",
            "tenant.py",
            "patient.py",
            "organization.py",
            "documents.py",
            "storage.py",
            "telemedicine.py",
            "appointments.py",
            "encounters.py",
        ):
            self.assertTrue((self.root / "integrations" / name).exists())

    def test_workflow_registry_contract(self):
        text = (self.root / "workflow_registry.py").read_text(encoding="utf-8")
        for name in (
            "notes.note.create",
            "notes.note.submit_review",
            "notes.note.sign",
            "notes.note.amend",
            "notes.note.cancel",
        ):
            self.assertIn(name, text)

    def test_domain_events_exist(self):
        text = (self.root / "events" / "note_events.py").read_text(encoding="utf-8")
        for name in (
            "ClinicalNoteCreatedEvent",
            "ClinicalNoteReviewedEvent",
            "ClinicalNoteSignedEvent",
            "ClinicalNoteAmendedEvent",
            "ClinicalNoteCancelledEvent",
        ):
            self.assertIn(name, text)

from django.apps import apps
from django.test import TestCase

from apps.notes.models import NoteTransition
from apps.notes.workflows import ClinicalNoteService


class ClinicalNoteWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tenant = apps.get_model("tenancy", "Tenant")
        Organization = apps.get_model("organizations", "Organization")
        cls.tenant = Tenant.objects.create(name="Notes Tenant", slug="notes-tenant")
        cls.organization = Organization.objects.create(
            tenant=cls.tenant, name="Notes Org", code="NOTES-ORG", slug="notes-org"
        )
        User = apps.get_model("accounts", "User")
        cls.user = User.objects.create_user(
            username="notes-user", email="notes@example.invalid", password="x"
        )
        cls.patient = apps.get_model("patient_core", "Patient").objects.create(
            organization=cls.organization,
            first_name="Test",
            last_name="Patient",
            date_of_birth="1985-01-15",
        )

    def test_full_note_lifecycle(self):
        note = ClinicalNoteService.create(
            organization=self.organization,
            patient=self.patient,
            author=self.user,
            title="Progress Note",
            body="Initial",
        )
        ClinicalNoteService.submit_for_review(
            note_id=note.note_id, organization_id=self.organization.id, actor=self.user
        )
        note = ClinicalNoteService.sign(
            note_id=note.note_id, organization_id=self.organization.id, actor=self.user
        )
        self.assertEqual(note.status, "signed")
        self.assertEqual(NoteTransition.objects.filter(note=note).count(), 2)

    def test_invalid_direct_sign_from_draft(self):
        note = ClinicalNoteService.create(
            organization=self.organization,
            patient=self.patient,
            author=self.user,
            title="Progress Note",
        )
        with self.assertRaises(ValueError):
            ClinicalNoteService.sign(
                note_id=note.note_id,
                organization_id=self.organization.id,
                actor=self.user,
            )

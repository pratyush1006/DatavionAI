"""
Tests for clinical note services.
"""

from __future__ import annotations

from apps.common.tests.base import BaseTestCase
from apps.notes.constants import NoteType, TemplateType
from apps.notes.models import ClinicalNote, NoteTemplate
from apps.notes.services import (
    NoteService,
    TemplateService,
)
from apps.notes.tests.factories import ClinicalNoteFactory, NoteTemplateFactory


class NoteServiceTestCase(BaseTestCase):
    """
    Test cases for NoteService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()
        self.note = ClinicalNoteFactory(
            organization=self.organization,
            patient=self.patient,
            note_type=NoteType.SOAP,
            title="Test Note",
            content={"subjective": "Patient feels well."},
        )

    def test_create_note(self) -> None:
        """
        Clinical note should be created successfully.
        """

        note = NoteService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "note_type": NoteType.PROGRESS_NOTE,
                "title": "New Progress Note",
                "content": {"objective": "Vitals stable."},
                "created_by": self.create_employee(),
            },
        )

        self.assertIsInstance(
            note,
            ClinicalNote,
        )

        self.assertEqual(
            note.title,
            "New Progress Note",
        )

    def test_create_note_persists_to_database(self) -> None:
        """
        Created note should be persisted.
        """

        initial_count = ClinicalNote.objects.count()

        NoteService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "note_type": NoteType.SOAP,
                "title": "Persisted Note",
                "content": {},
                "created_by": self.create_employee(),
            },
        )

        self.assertEqual(
            ClinicalNote.objects.count(),
            initial_count + 1,
        )

    def test_update_note(self) -> None:
        """
        Clinical note should be updated successfully.
        """

        updated_note = NoteService.update(
            instance=self.note,
            validated_data={
                "title": "Updated Title",
            },
        )

        updated_note.refresh_from_db()

        self.assertEqual(
            updated_note.title,
            "Updated Title",
        )

    def test_sign_note(self) -> None:
        """
        Clinical note should be signed successfully.
        """

        employee = self.create_employee()

        signed_note = NoteService.sign(
            note_id=self.note.id,
            signed_by=employee,
        )

        signed_note.refresh_from_db()

        self.assertIsNotNone(
            signed_note.signed_at,
        )

        self.assertEqual(
            signed_note.signed_by,
            employee,
        )

    def test_amend_note(self) -> None:
        """
        Clinical note should be amended successfully.
        """

        amended_note = NoteService.amend(
            note_id=self.note.id,
            amendment_reason="Added more details.",
            updated_content={
                "subjective": "Patient feels better after medication.",
            },
            amended_by=self.create_employee(),
        )

        amended_note.refresh_from_db()

        self.assertTrue(
            amended_note.is_amended,
        )

        self.assertEqual(
            amended_note.original_note,
            self.note,
        )

        self.assertEqual(
            amended_note.amendment_reason,
            "Added more details.",
        )

        self.note.refresh_from_db()

        self.assertTrue(
            self.note.is_amended,
        )

    def test_bulk_create_notes(self) -> None:
        """
        Multiple clinical notes should be created successfully.
        """

        validated_data_list = [
            {
                "organization": self.organization,
                "patient": self.patient,
                "note_type": NoteType.SOAP,
                "title": f"Bulk Note {i}",
                "content": {},
                "created_by": self.create_employee(),
            }
            for i in range(3)
        ]

        notes = NoteService.bulk_create(
            validated_data_list=validated_data_list,
        )

        self.assertEqual(
            len(notes),
            3,
        )

        self.assertEqual(
            ClinicalNote.objects.filter(
                title__startswith="Bulk Note",
            ).count(),
            3,
        )


class TemplateServiceTestCase(BaseTestCase):
    """
    Test cases for TemplateService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.template = NoteTemplateFactory(
            organization=self.organization,
            name="SOAP Template",
            template_type=TemplateType.SOAP,
        )

    def test_create_template(self) -> None:
        """
        Note template should be created successfully.
        """

        template = TemplateService.create(
            validated_data={
                "organization": self.organization,
                "name": "Progress Note Template",
                "template_type": TemplateType.PROGRESS_NOTE,
                "content": {"sections": ["subjective", "objective"]},
            },
        )

        self.assertIsInstance(
            template,
            NoteTemplate,
        )

        self.assertEqual(
            template.name,
            "Progress Note Template",
        )

    def test_create_template_persists_to_database(self) -> None:
        """
        Created template should be persisted.
        """

        initial_count = NoteTemplate.objects.count()

        TemplateService.create(
            validated_data={
                "organization": self.organization,
                "name": "Persisted Template",
                "template_type": TemplateType.OTHER,
                "content": {},
            },
        )

        self.assertEqual(
            NoteTemplate.objects.count(),
            initial_count + 1,
        )

    def test_update_template(self) -> None:
        """
        Note template should be updated successfully.
        """

        updated_template = TemplateService.update(
            instance=self.template,
            validated_data={
                "name": "Updated Template Name",
            },
        )

        updated_template.refresh_from_db()

        self.assertEqual(
            updated_template.name,
            "Updated Template Name",
        )

    def test_activate_template(self) -> None:
        """
        Note template should be activated successfully.
        """

        self.template.is_active = False
        self.template.save()

        activated_template = TemplateService.activate(
            instance=self.template,
        )

        activated_template.refresh_from_db()

        self.assertTrue(
            activated_template.is_active,
        )

    def test_deactivate_template(self) -> None:
        """
        Note template should be deactivated successfully.
        """

        deactivated_template = TemplateService.deactivate(
            instance=self.template,
        )

        deactivated_template.refresh_from_db()

        self.assertFalse(
            deactivated_template.is_active,
        )

    def test_bulk_create_templates(self) -> None:
        """
        Multiple note templates should be created successfully.
        """

        validated_data_list = [
            {
                "organization": self.organization,
                "name": f"Bulk Template {i}",
                "template_type": TemplateType.OTHER,
                "content": {},
            }
            for i in range(3)
        ]

        templates = TemplateService.bulk_create(
            validated_data_list=validated_data_list,
        )

        self.assertEqual(
            len(templates),
            3,
        )

        self.assertEqual(
            NoteTemplate.objects.filter(
                name__startswith="Bulk Template",
            ).count(),
            3,
        )


__all__ = [
    "NoteServiceTestCase",
    "TemplateServiceTestCase",
]

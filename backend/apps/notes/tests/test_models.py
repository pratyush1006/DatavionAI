"""
Tests for the NoteTemplate and ClinicalNote models.
"""

from __future__ import annotations

from apps.common.tests.base import BaseTestCase
from apps.notes.constants import NoteType, TemplateType
from apps.notes.models import ClinicalNote, NoteTemplate
from apps.notes.tests.factories import ClinicalNoteFactory, NoteTemplateFactory


class NoteTemplateModelTestCase(BaseTestCase):
    """
    Test cases for the NoteTemplate model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.template = NoteTemplateFactory(
            organization=self.organization,
            name="SOAP Template",
            template_type=TemplateType.SOAP,
        )

    def test_template_creation(self) -> None:
        """
        NoteTemplate should be created successfully.
        """

        self.assertEqual(
            self.template.organization,
            self.organization,
        )

        self.assertEqual(
            self.template.name,
            "SOAP Template",
        )

        self.assertEqual(
            self.template.template_type,
            TemplateType.SOAP,
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the template display name.
        """

        self.assertEqual(
            str(self.template),
            "SOAP Template (SOAP)",
        )

    def test_default_is_active(self) -> None:
        """
        Default is_active should be True.
        """

        self.assertTrue(
            self.template.is_active,
        )

    def test_default_is_system_template(self) -> None:
        """
        Default is_system_template should be False.
        """

        self.assertFalse(
            self.template.is_system_template,
        )

    def test_meta_table_name(self) -> None:
        """
        NoteTemplate model should use the configured database table.
        """

        self.assertEqual(
            NoteTemplate._meta.db_table,
            "note_templates",
        )

    def test_meta_ordering(self) -> None:
        """
        NoteTemplate model should use the configured ordering.
        """

        self.assertEqual(
            NoteTemplate._meta.ordering,
            ("name",),
        )


class ClinicalNoteModelTestCase(BaseTestCase):
    """
    Test cases for the ClinicalNote model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.note = ClinicalNoteFactory(
            organization=self.organization,
            patient=self.create_patient(),
            note_type=NoteType.SOAP,
            title="Initial SOAP Note",
        )

    def test_note_creation(self) -> None:
        """
        ClinicalNote should be created successfully.
        """

        self.assertEqual(
            self.note.organization,
            self.organization,
        )

        self.assertEqual(
            self.note.title,
            "Initial SOAP Note",
        )

        self.assertEqual(
            self.note.note_type,
            NoteType.SOAP,
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the note display string.
        """

        self.assertIn(
            self.note.title,
            str(self.note),
        )

    def test_default_is_amended(self) -> None:
        """
        Default is_amended should be False.
        """

        self.assertFalse(
            self.note.is_amended,
        )

    def test_default_signed_at(self) -> None:
        """
        Default signed_at should be None.
        """

        self.assertIsNone(
            self.note.signed_at,
        )

    def test_meta_table_name(self) -> None:
        """
        ClinicalNote model should use the configured database table.
        """

        self.assertEqual(
            ClinicalNote._meta.db_table,
            "clinical_notes",
        )

    def test_meta_ordering(self) -> None:
        """
        ClinicalNote model should use the configured ordering.
        """

        self.assertEqual(
            ClinicalNote._meta.ordering,
            ("-created_at",),
        )

    def test_raw_text_can_be_blank(self) -> None:
        """
        raw_text should default to blank.
        """

        self.assertEqual(
            self.note.raw_text,
            "",
        )

    def test_amendment_reason_can_be_blank(self) -> None:
        """
        amendment_reason should default to blank.
        """

        self.assertEqual(
            self.note.amendment_reason,
            "",
        )

    def test_foreign_key_relationships(self) -> None:
        """
        ClinicalNote should have the correct foreign key relationships.
        """

        self.assertEqual(
            self.note.organization,
            self.organization,
        )

        self.assertIsNotNone(
            self.note.patient,
        )

        self.assertIsNotNone(
            self.note.created_by,
        )


__all__ = [
    "ClinicalNoteModelTestCase",
    "NoteTemplateModelTestCase",
]

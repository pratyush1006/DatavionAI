"""
Tests for clinical note selectors.
"""

from __future__ import annotations

from apps.common.tests.base import BaseTestCase
from apps.notes.constants import NoteType, TemplateType
from apps.notes.selectors import NoteSelector, TemplateSelector
from apps.notes.tests.factories import ClinicalNoteFactory, NoteTemplateFactory


class NoteSelectorTestCase(BaseTestCase):
    """
    Test cases for NoteSelector.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.active_note = ClinicalNoteFactory(
            organization=self.organization,
            patient=self.patient,
            note_type=NoteType.SOAP,
            title="Active Note",
        )

        self.another_note = ClinicalNoteFactory(
            organization=self.organization,
            patient=self.patient,
            note_type=NoteType.PROGRESS_NOTE,
            title="Another Note",
        )

    def test_queryset(self) -> None:
        """
        queryset() should return a queryset.
        """

        queryset = NoteSelector.queryset()

        self.assertIn(
            self.active_note,
            queryset,
        )

    def test_get(self) -> None:
        """
        get() should return the requested clinical note.
        """

        note = NoteSelector.get(
            note_id=self.active_note.id,
        )

        self.assertEqual(
            note,
            self.active_note,
        )

    def test_list(self) -> None:
        """
        list() should return all clinical notes.
        """

        notes = NoteSelector.list()

        self.assertEqual(
            notes.count(),
            2,
        )

    def test_list_by_patient(self) -> None:
        """
        list_by_patient() should return notes for a specific patient.
        """

        notes = NoteSelector.list_by_patient(
            patient_id=self.patient.id,
        )

        self.assertEqual(
            notes.count(),
            2,
        )

    def test_list_by_organization(self) -> None:
        """
        list_by_organization() should filter by organization.
        """

        notes = NoteSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertEqual(
            notes.count(),
            2,
        )

    def test_search(self) -> None:
        """
        search() should find matching clinical notes.
        """

        notes = NoteSelector.search(
            organization=self.organization,
            query="Active",
        )

        self.assertEqual(
            notes.count(),
            1,
        )

        self.assertEqual(
            notes.first(),
            self.active_note,
        )

    def test_count(self) -> None:
        """
        count() should return the clinical note count.
        """

        self.assertEqual(
            NoteSelector.count(
                organization=self.organization,
            ),
            2,
        )

    def test_list_signed(self) -> None:
        """
        list_signed() should return signed clinical notes.
        """

        from django.utils import timezone

        employee = self.create_employee()

        self.active_note.signed_at = timezone.now()
        self.active_note.signed_by = employee
        self.active_note.save()

        notes = NoteSelector.list_signed(
            organization=self.organization,
        )

        self.assertEqual(
            notes.count(),
            1,
        )

    def test_list_unsigned(self) -> None:
        """
        list_unsigned() should return unsigned clinical notes.
        """

        notes = NoteSelector.list_unsigned(
            organization=self.organization,
        )

        self.assertEqual(
            notes.count(),
            2,
        )


class TemplateSelectorTestCase(BaseTestCase):
    """
    Test cases for TemplateSelector.
    """

    def setUp(self) -> None:
        super().setUp()

        self.active_template = NoteTemplateFactory(
            organization=self.organization,
            name="SOAP Template",
            template_type=TemplateType.SOAP,
        )

        self.inactive_template = NoteTemplateFactory(
            organization=self.organization,
            name="Inactive Template",
            template_type=TemplateType.OTHER,
            is_active=False,
        )

    def test_queryset(self) -> None:
        """
        queryset() should return a queryset.
        """

        queryset = TemplateSelector.queryset()

        self.assertIn(
            self.active_template,
            queryset,
        )

    def test_get(self) -> None:
        """
        get() should return the requested note template.
        """

        template = TemplateSelector.get(
            template_id=self.active_template.id,
        )

        self.assertEqual(
            template,
            self.active_template,
        )

    def test_list(self) -> None:
        """
        list() should return all note templates.
        """

        templates = TemplateSelector.list()

        self.assertEqual(
            templates.count(),
            2,
        )

    def test_list_by_organization(self) -> None:
        """
        list_by_organization() should filter by organization.
        """

        templates = TemplateSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertEqual(
            templates.count(),
            2,
        )

    def test_list_by_type(self) -> None:
        """
        list_by_type() should filter by template type.
        """

        templates = TemplateSelector.list_by_type(
            organization=self.organization,
            template_type=TemplateType.SOAP,
        )

        self.assertEqual(
            templates.count(),
            1,
        )

        self.assertEqual(
            templates.first(),
            self.active_template,
        )

    def test_search(self) -> None:
        """
        search() should find matching note templates.
        """

        templates = TemplateSelector.search(
            organization=self.organization,
            query="SOAP",
        )

        self.assertEqual(
            templates.count(),
            1,
        )

        self.assertEqual(
            templates.first(),
            self.active_template,
        )

    def test_count(self) -> None:
        """
        count() should return the note template count.
        """

        self.assertEqual(
            TemplateSelector.count(
                organization=self.organization,
            ),
            2,
        )


__all__ = [
    "NoteSelectorTestCase",
    "TemplateSelectorTestCase",
]

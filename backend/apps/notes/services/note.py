"""
Clinical note services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.notes.models import ClinicalNote, NoteTemplate
from apps.notes.selectors import NoteSelector
from apps.platform.accounts.models import User


class NoteService:
    """
    Application service responsible for clinical note write operations.

    This service is the single entry point for all clinical note lifecycle
    operations and provides a centralized location for future business
    rules such as:

    - Note signing and verification
    - Amendment tracking
    - Voice-to-text processing
    - Template population
    - Audit logging
    - Domain events
    - Notifications
    - External integrations
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> ClinicalNote:
        """
        Create a new clinical note.
        """

        note = ClinicalNote(
            **validated_data,
        )

        note.full_clean()

        note.save()

        return note

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: ClinicalNote,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> ClinicalNote:
        """
        Update an existing clinical note.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def sign(
        *,
        note_id: Any,
        signed_by: Any,
    ) -> ClinicalNote:
        """
        Sign a clinical note.
        """

        note = NoteSelector.get(
            note_id=note_id,
        )

        note.signed_at = timezone.now()
        note.signed_by = signed_by

        note.full_clean()

        note.save(
            update_fields=[
                "signed_at",
                "signed_by",
            ],
        )

        return note

    @staticmethod
    @transaction.atomic
    def amend(
        *,
        note_id: Any,
        amendment_reason: str,
        updated_content: Mapping[str, Any],
        amended_by: Any,
    ) -> ClinicalNote:
        """
        Amend a clinical note by creating a new version.
        """

        original_note = NoteSelector.get(
            note_id=note_id,
        )

        amended_note = ClinicalNote(
            organization=original_note.organization,
            patient=original_note.patient,
            encounter=original_note.encounter,
            note_type=original_note.note_type,
            title=original_note.title,
            content=updated_content,
            raw_text=original_note.raw_text,
            is_amended=True,
            amendment_reason=amendment_reason,
            original_note=original_note,
            created_by=amended_by,
        )

        amended_note.full_clean()

        amended_note.save()

        original_note.is_amended = True

        original_note.save(
            update_fields=[
                "is_amended",
            ],
        )

        return amended_note

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[ClinicalNote]:
        """
        Create multiple clinical notes.
        """

        notes: list[ClinicalNote] = []

        for validated_data in validated_data_list:
            note = ClinicalNote(
                **validated_data,
            )

            note.full_clean()

            note.save()

            notes.append(note)

        return notes


class TemplateService:
    """
    Application service responsible for note template write operations.

    This service is the single entry point for all note template lifecycle
    operations and provides a centralized location for future business
    rules such as:

    - Template versioning
    - System template protection
    - Template validation
    - Audit logging
    - Domain events
    - Notifications
    - External integrations
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> NoteTemplate:
        """
        Create a new note template.
        """

        template = NoteTemplate(
            **validated_data,
        )

        template.full_clean()

        template.save()

        return template

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: NoteTemplate,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> NoteTemplate:
        """
        Update an existing note template.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: NoteTemplate,
        performed_by: User | None = None,
    ) -> NoteTemplate:
        """
        Activate a note template.
        """

        instance.is_active = True

        instance.full_clean()

        instance.save(
            update_fields=[
                "is_active",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        instance: NoteTemplate,
        performed_by: User | None = None,
    ) -> NoteTemplate:
        """
        Deactivate a note template.
        """

        instance.is_active = False

        instance.full_clean()

        instance.save(
            update_fields=[
                "is_active",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[NoteTemplate]:
        """
        Create multiple note templates.
        """

        templates: list[NoteTemplate] = []

        for validated_data in validated_data_list:
            template = NoteTemplate(
                **validated_data,
            )

            template.full_clean()

            template.save()

            templates.append(template)

        return templates


# ---------------------------------------------------------------------
# Backward compatibility aliases
# ---------------------------------------------------------------------

create_note = NoteService.create

update_note = NoteService.update

sign_note = NoteService.sign

amend_note = NoteService.amend

create_template = TemplateService.create

update_template = TemplateService.update

activate_template = TemplateService.activate

deactivate_template = TemplateService.deactivate


__all__ = [
    "NoteService",
    "TemplateService",
    "amend_note",
    "create_note",
    "create_template",
    "deactivate_template",
    "sign_note",
    "update_note",
    "update_template",
    "activate_template",
]

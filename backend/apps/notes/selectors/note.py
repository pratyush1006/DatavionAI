"""
Note selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.notes.models import ClinicalNote, NoteTemplate
from apps.platform.organizations.models import Organization


class NoteSelector:
    """
    Read-only queries for clinical notes.

    This selector centralizes all clinical note retrieval logic.
    No write operations should be implemented here.
    """

    @staticmethod
    def queryset() -> QuerySet[ClinicalNote]:
        """
        Return the base clinical note queryset.
        """

        return ClinicalNote.objects.select_related(
            "organization",
            "patient",
            "encounter",
            "signed_by",
            "created_by",
            "original_note",
        )

    @staticmethod
    def list() -> QuerySet[ClinicalNote]:
        """
        Return all clinical notes.
        """

        return NoteSelector.queryset()

    @staticmethod
    def get(
        *,
        note_id: UUID,
    ) -> ClinicalNote:
        """
        Return a clinical note by identifier.
        """

        return get_object_or_404(
            NoteSelector.queryset(),
            pk=note_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[ClinicalNote]:
        """
        Return clinical notes for a specific patient.
        """

        return NoteSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_encounter(
        *,
        encounter_id: UUID,
    ) -> QuerySet[ClinicalNote]:
        """
        Return clinical notes for a specific encounter.
        """

        return NoteSelector.queryset().filter(
            encounter_id=encounter_id,
        )

    @staticmethod
    def list_by_author(
        *,
        author_id: UUID,
    ) -> QuerySet[ClinicalNote]:
        """
        Return clinical notes created by a specific author.
        """

        return NoteSelector.queryset().filter(
            created_by_id=author_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[ClinicalNote]:
        """
        Return all clinical notes belonging to an organization.
        """

        return NoteSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def search(
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[ClinicalNote]:
        """
        Search clinical notes within an organization.
        """

        return (
            NoteSelector.queryset()
            .filter(
                organization=organization,
            )
            .filter(
                Q(
                    title__icontains=query,
                )
                | Q(
                    raw_text__icontains=query,
                )
                | Q(
                    content__icontains=query,
                )
            )
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of clinical notes within an organization.
        """

        return NoteSelector.list_by_organization(
            organization=organization,
        ).count()

    @staticmethod
    def list_signed(
        *,
        organization: Organization,
    ) -> QuerySet[ClinicalNote]:
        """
        Return signed clinical notes within an organization.
        """

        return NoteSelector.list_by_organization(
            organization=organization,
        ).filter(
            signed_at__isnull=False,
        )

    @staticmethod
    def list_unsigned(
        *,
        organization: Organization,
    ) -> QuerySet[ClinicalNote]:
        """
        Return unsigned clinical notes within an organization.
        """

        return NoteSelector.list_by_organization(
            organization=organization,
        ).filter(
            signed_at__isnull=True,
        )


class TemplateSelector:
    """
    Read-only queries for note templates.

    This selector centralizes all note template retrieval logic.
    No write operations should be implemented here.
    """

    @staticmethod
    def queryset() -> QuerySet[NoteTemplate]:
        """
        Return the base note template queryset.
        """

        return NoteTemplate.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[NoteTemplate]:
        """
        Return all note templates.
        """

        return TemplateSelector.queryset()

    @staticmethod
    def get(
        *,
        template_id: UUID,
    ) -> NoteTemplate:
        """
        Return a note template by identifier.
        """

        return get_object_or_404(
            TemplateSelector.queryset(),
            pk=template_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[NoteTemplate]:
        """
        Return all note templates belonging to an organization.
        """

        return TemplateSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_by_type(
        *,
        organization: Organization,
        template_type: str,
    ) -> QuerySet[NoteTemplate]:
        """
        Return note templates of a specific type within an organization.
        """

        return TemplateSelector.list_by_organization(
            organization=organization,
        ).filter(
            template_type=template_type,
        )

    @staticmethod
    def search(
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[NoteTemplate]:
        """
        Search note templates within an organization.
        """

        return (
            TemplateSelector.queryset()
            .filter(
                organization=organization,
            )
            .filter(
                Q(
                    name__icontains=query,
                )
                | Q(
                    content__icontains=query,
                )
            )
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of note templates within an organization.
        """

        return TemplateSelector.list_by_organization(
            organization=organization,
        ).count()


# ---------------------------------------------------------------------
# Backward compatibility aliases
# ---------------------------------------------------------------------

get_notes = NoteSelector.list

get_note_by_id = NoteSelector.get

get_organization_notes = NoteSelector.list_by_organization

get_templates = TemplateSelector.list

get_template_by_id = TemplateSelector.get

get_organization_templates = TemplateSelector.list_by_organization


__all__ = [
    "NoteSelector",
    "TemplateSelector",
    "get_note_by_id",
    "get_notes",
    "get_organization_notes",
    "get_template_by_id",
    "get_templates",
    "get_organization_templates",
]

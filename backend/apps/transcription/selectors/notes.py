"""
Tenant-scoped generated-note selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.transcription.models import GeneratedNote


class GeneratedNoteSelector:
    @staticmethod
    def queryset(*, organization_id) -> QuerySet[GeneratedNote]:
        return GeneratedNote.objects.select_related(
            "organization",
            "job",
            "patient",
            "encounter",
            "clinical_note",
            "reviewed_by",
        ).filter(organization_id=organization_id)

    @classmethod
    def get(cls, *, note_id, organization_id) -> GeneratedNote:
        return cls.queryset(
            organization_id=organization_id,
        ).get(note_id=note_id)

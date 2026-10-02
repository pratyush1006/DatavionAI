from django.db.models import QuerySet

from apps.notes.models import ClinicalNote


class ClinicalNoteSelector:
    @staticmethod
    def queryset(*, organization_id) -> QuerySet[ClinicalNote]:
        return ClinicalNote.objects.select_related(
            "organization", "patient", "encounter", "author", "signed_by"
        ).filter(organization_id=organization_id)

    @classmethod
    def get(cls, *, note_id, organization_id):
        return cls.queryset(organization_id=organization_id).get(note_id=note_id)

from apps.notes.models import ClinicalNoteTemplate


class ClinicalNoteTemplateSelector:
    @staticmethod
    def active(*, organization_id):
        return ClinicalNoteTemplate.objects.filter(
            organization_id=organization_id, is_active=True
        ).order_by("name")

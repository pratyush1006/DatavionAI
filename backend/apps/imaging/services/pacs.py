from apps.imaging.models import ImagingStudyReference


def pacs_references(*, tenant_id, study_id):
    return ImagingStudyReference.objects.filter(
        tenant_id=tenant_id, study_id=study_id
    ).order_by("created_at")

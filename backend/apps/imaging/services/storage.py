from apps.imaging.models import ImagingStudyReference


def storage_references(*, tenant_id, study_id):
    return ImagingStudyReference.objects.filter(
        tenant_id=tenant_id, study_id=study_id
    ).order_by("created_at")

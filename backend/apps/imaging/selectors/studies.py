from apps.imaging.models import ImagingStudy


def get_study(*, tenant_id, study_id):
    return ImagingStudy.objects.select_related("order", "procedure").get(
        tenant_id=tenant_id, id=study_id
    )

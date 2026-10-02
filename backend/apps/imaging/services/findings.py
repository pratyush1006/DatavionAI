from apps.imaging.models import ImagingFinding


def findings_for_study(*, tenant_id, study_id):
    return ImagingFinding.objects.filter(
        tenant_id=tenant_id, study_id=study_id
    ).order_by("created_at")

from apps.imaging.models import ImagingStudy


def acquisition_worklist(*, tenant_id):
    return ImagingStudy.objects.filter(
        tenant_id=tenant_id, status__in=["scheduled", "arrived", "ready", "acquiring"]
    ).order_by("created_at")

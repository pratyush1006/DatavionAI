from apps.imaging.models import ImagingStudy


def worklist_for_tenant(*, tenant_id, statuses=None):
    queryset = ImagingStudy.objects.select_related(
        "order", "procedure", "procedure__modality"
    ).filter(tenant_id=tenant_id)
    if statuses:
        queryset = queryset.filter(status__in=statuses)
    return queryset.order_by("order__priority", "created_at")

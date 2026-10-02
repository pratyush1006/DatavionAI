from apps.imaging.models import ImagingOrder


def ready_worklist(*, tenant_id):
    return ImagingOrder.objects.filter(tenant_id=tenant_id, status="ready").order_by(
        "created_at"
    )

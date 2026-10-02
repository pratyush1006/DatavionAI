from apps.imaging.models import ImagingOrder


def get_order(*, tenant_id, order_id):
    return ImagingOrder.objects.get(tenant_id=tenant_id, id=order_id)

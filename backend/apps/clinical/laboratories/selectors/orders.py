from ..models import (
    LaboratoryOrder,
)


def orders(organization_id):
    return LaboratoryOrder.objects.filter(
        organization_id=organization_id, is_deleted=False
    ).prefetch_related("items", "specimens")

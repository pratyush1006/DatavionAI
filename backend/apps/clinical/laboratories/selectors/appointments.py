from ..models import (
    LaboratorySlot,
)


def slots(laboratory_id):
    return LaboratorySlot.objects.filter(
        laboratory_id=laboratory_id, is_deleted=False
    ).order_by("starts_at")

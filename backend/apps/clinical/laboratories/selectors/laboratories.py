from ..models import (
    Laboratory,
)


def laboratories(organization_id):
    return Laboratory.objects.filter(organization_id=organization_id, is_deleted=False)

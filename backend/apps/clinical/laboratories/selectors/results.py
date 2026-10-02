from ..models import (
    LaboratoryResult,
)


def results(organization_id):
    return LaboratoryResult.objects.filter(
        organization_id=organization_id, is_deleted=False
    )

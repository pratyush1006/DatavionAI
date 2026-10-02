from ..models import (
    LaboratoryTest,
)


def tests(organization_id):
    return LaboratoryTest.objects.filter(
        organization_id=organization_id, is_deleted=False
    )

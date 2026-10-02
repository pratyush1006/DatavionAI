from ..models import (
    LaboratoryReport,
)


def reports(organization_id):
    return LaboratoryReport.objects.filter(
        organization_id=organization_id, is_deleted=False
    )

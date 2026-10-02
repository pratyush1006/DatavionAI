from django.db import transaction

from ..models import LaboratoryIdempotencyRecord


@transaction.atomic
def get_or_create_request(
    *,
    organization_id,
    key,
    operation,
    response_payload=None,
    resource_type="",
    resource_id=None,
):
    return LaboratoryIdempotencyRecord.objects.get_or_create(
        organization_id=organization_id,
        key=key,
        operation=operation,
        defaults={
            "response_payload": response_payload or {},
            "resource_type": resource_type,
            "resource_id": resource_id,
        },
    )

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.imaging.models import ImagingIdempotencyKey


def claim_idempotency_key(*, tenant_id, key, operation, entity_type="", entity_id=None):
    key = str(key or "").strip()
    operation = str(operation or "").strip()
    if not key:
        raise ValidationError("Idempotency key is required for this operation.")
    if not operation:
        raise ValidationError("Idempotency operation is required.")
    existing = (
        ImagingIdempotencyKey.objects.select_for_update()
        .filter(tenant_id=tenant_id, key=key, operation=operation)
        .first()
    )
    if existing:
        return existing, False
    try:
        with transaction.atomic():
            return (
                ImagingIdempotencyKey.objects.create(
                    tenant_id=tenant_id,
                    key=key,
                    operation=operation,
                    entity_type=entity_type,
                    entity_id=entity_id,
                ),
                True,
            )
    except IntegrityError:
        return (
            ImagingIdempotencyKey.objects.select_for_update().get(
                tenant_id=tenant_id, key=key, operation=operation
            ),
            False,
        )


@transaction.atomic
def execute_idempotent(
    *, tenant_id, key, operation, callback, entity_type="", entity_id=None
):
    record, created = claim_idempotency_key(
        tenant_id=tenant_id,
        key=key,
        operation=operation,
        entity_type=entity_type,
        entity_id=entity_id,
    )
    if not created:
        if record.response_payload:
            return (
                record.response_payload.get("payload", {}),
                int(record.response_payload.get("status_code", 200)),
                True,
            )
        raise ValidationError(
            "An idempotent Imaging operation with this key is already in progress."
        )
    payload, status_code = callback()
    record.response_payload = {"payload": payload, "status_code": int(status_code)}
    record.save(update_fields=("response_payload", "updated_at"))
    return payload, int(status_code), False

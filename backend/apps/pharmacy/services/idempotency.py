from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.pharmacy.models import PharmacyIdempotencyKey


def claim_idempotency_key(*, organization, key, operation):
    key = str(key or "").strip()
    operation = str(operation or "").strip()
    if not key:
        raise ValidationError("Idempotency key is required for this operation.")
    if len(key) > 160:
        raise ValidationError("Idempotency key exceeds the 160 character limit.")
    if not operation:
        raise ValidationError("Idempotency operation is required.")
    existing = (
        PharmacyIdempotencyKey.objects.select_for_update()
        .filter(organization=organization, key=key, operation=operation)
        .first()
    )
    if existing is not None:
        return existing, False
    try:
        with transaction.atomic():
            return (
                PharmacyIdempotencyKey.objects.create(
                    organization=organization, key=key, operation=operation
                ),
                True,
            )
    except IntegrityError:
        existing = PharmacyIdempotencyKey.objects.select_for_update().get(
            organization=organization, key=key, operation=operation
        )
        return existing, False


@transaction.atomic
def execute_idempotent(*, organization, key, operation, callback):
    """Execute a mutation once and persist a replayable response atomically."""
    record, created = claim_idempotency_key(
        organization=organization, key=key, operation=operation
    )
    if not created:
        if record.response_payload:
            return (
                record.response_payload.get("payload", {}),
                int(record.response_payload.get("status_code", 200)),
                True,
            )
        raise ValidationError(
            "An idempotent operation with this key is already in progress."
        )

    payload, status_code = callback()
    record.response_payload = {"payload": payload, "status_code": int(status_code)}
    record.save(update_fields=("response_payload", "updated_at"))
    return payload, int(status_code), False

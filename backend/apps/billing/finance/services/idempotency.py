from django.db import transaction

from apps.billing.finance.models import FinanceIdempotencyKey


def execute_idempotent(*, organization, workflow, key, execute):
    key = str(key or "").strip()
    if not key:
        raise ValueError("Idempotency-Key is required.")
    with transaction.atomic():
        existing = (
            FinanceIdempotencyKey.objects.select_for_update()
            .filter(organization=organization, workflow=workflow, key=key)
            .first()
        )
        if existing:
            return existing.response, True
        result = execute()
        response = {"entity_id": str(getattr(result, "pk", "")), "workflow": workflow}
        FinanceIdempotencyKey.objects.create(
            organization=organization, workflow=workflow, key=key, response=response
        )
        return result, False

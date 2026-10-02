from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.billing.finance.models import FinanceOutboxEvent


def enqueue_event(
    *, organization, event_type, aggregate_type, aggregate_id=None, payload=None
):
    return FinanceOutboxEvent.objects.create(
        organization=organization,
        event_type=event_type,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        payload=payload or {},
    )


def _claim(now=None):
    now = now or timezone.now()
    with transaction.atomic():
        event = (
            FinanceOutboxEvent.objects.select_for_update(skip_locked=True)
            .filter(status=FinanceOutboxEvent.Status.PENDING, available_at__lte=now)
            .order_by("available_at", "created_at", "id")
            .first()
        )
        if event is None:
            event = (
                FinanceOutboxEvent.objects.select_for_update(skip_locked=True)
                .filter(
                    status=FinanceOutboxEvent.Status.PROCESSING, locked_until__lte=now
                )
                .order_by("available_at", "created_at", "id")
                .first()
            )
        if event is None:
            return None
        event.status = FinanceOutboxEvent.Status.PROCESSING
        event.attempts += 1
        event.locked_until = now + timedelta(minutes=5)
        event.save(update_fields=("status", "attempts", "locked_until", "updated_at"))
        return event


def publish_pending_events(*, limit=100, publisher=None, now=None, max_attempts=5):
    publisher = publisher or (lambda envelope: None)
    published = 0
    for _ in range(max(0, int(limit))):
        event = _claim(now=now)
        if event is None:
            break
        envelope = {
            "event_id": str(event.event_id),
            "event_type": event.event_type,
            "aggregate_type": event.aggregate_type,
            "aggregate_id": str(event.aggregate_id) if event.aggregate_id else None,
            "organization_id": str(event.organization_id),
            "payload": event.payload,
        }
        try:
            publisher(envelope)
        except Exception as exc:
            if event.attempts >= max_attempts:
                FinanceOutboxEvent.objects.filter(pk=event.pk).update(
                    status=FinanceOutboxEvent.Status.FAILED,
                    locked_until=None,
                    last_error=str(exc)[:4000],
                )
            else:
                delay = min(300, 2 ** min(event.attempts, 8))
                FinanceOutboxEvent.objects.filter(pk=event.pk).update(
                    status=FinanceOutboxEvent.Status.PENDING,
                    available_at=timezone.now() + timedelta(seconds=delay),
                    locked_until=None,
                    last_error=str(exc)[:4000],
                )
            continue
        FinanceOutboxEvent.objects.filter(pk=event.pk).update(
            status=FinanceOutboxEvent.Status.PUBLISHED,
            published_at=timezone.now(),
            locked_until=None,
            last_error="",
        )
        published += 1
    return published

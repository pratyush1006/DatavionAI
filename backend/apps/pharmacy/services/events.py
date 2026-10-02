from datetime import timedelta
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from apps.pharmacy.models import PharmacyOutboxEvent

MAX_EVENT_ATTEMPTS = 8
PROCESSING_LEASE_MINUTES = 5
MAX_RETRY_SECONDS = 60


def enqueue_event(
    *,
    organization,
    event_type,
    aggregate_type,
    aggregate_id=None,
    payload=None,
    event_id=None,
):
    return PharmacyOutboxEvent.objects.create(
        organization=organization,
        event_id=event_id or uuid4(),
        event_type=str(event_type),
        aggregate_type=str(aggregate_type),
        aggregate_id=aggregate_id,
        payload=payload or {},
    )


def _claim_event(*, now=None):
    now = now or timezone.now()
    with transaction.atomic():
        queryset = PharmacyOutboxEvent.objects.select_for_update().filter(
            status=PharmacyOutboxEvent.Status.PENDING,
            available_at__lte=now,
        ) | PharmacyOutboxEvent.objects.select_for_update().filter(
            status=PharmacyOutboxEvent.Status.PROCESSING,
            locked_until__lte=now,
        )
        event = queryset.order_by("available_at", "created_at").first()
        if event is None:
            return None
        event.status = PharmacyOutboxEvent.Status.PROCESSING
        event.attempts += 1
        event.locked_until = now + timedelta(minutes=PROCESSING_LEASE_MINUTES)
        event.save(update_fields=["status", "attempts", "locked_until", "updated_at"])
        return event


def _envelope(event):
    return {
        "event_id": str(event.event_id),
        "event_type": event.event_type,
        "aggregate_type": event.aggregate_type,
        "aggregate_id": str(event.aggregate_id) if event.aggregate_id else None,
        "organization_id": str(event.organization_id),
        "payload": event.payload,
    }


def publish_pending_events(*, limit=100, publisher=None, now=None):
    """Publish committed outbox records with bounded retries and a DLQ state.

    Delivery is at-least-once. Publishers must therefore deduplicate by
    ``event_id``. After MAX_EVENT_ATTEMPTS, an event becomes FAILED and needs
    explicit operational replay rather than retrying forever.
    """
    if limit <= 0:
        return 0
    if publisher is None:
        publisher = lambda envelope: None
    published = 0
    for _ in range(int(limit)):
        event = _claim_event(now=now)
        if event is None:
            break
        try:
            publisher(_envelope(event))
        except Exception as exc:
            if event.attempts >= MAX_EVENT_ATTEMPTS:
                PharmacyOutboxEvent.objects.filter(
                    pk=event.pk, status=PharmacyOutboxEvent.Status.PROCESSING
                ).update(
                    status=PharmacyOutboxEvent.Status.FAILED,
                    locked_until=None,
                    last_error=str(exc)[:4000],
                )
            else:
                delay = min(MAX_RETRY_SECONDS, 2 ** min(event.attempts, 6))
                PharmacyOutboxEvent.objects.filter(
                    pk=event.pk, status=PharmacyOutboxEvent.Status.PROCESSING
                ).update(
                    status=PharmacyOutboxEvent.Status.PENDING,
                    available_at=timezone.now() + timedelta(seconds=delay),
                    locked_until=None,
                    last_error=str(exc)[:4000],
                )
            continue
        PharmacyOutboxEvent.objects.filter(
            pk=event.pk, status=PharmacyOutboxEvent.Status.PROCESSING
        ).update(
            status=PharmacyOutboxEvent.Status.PUBLISHED,
            published_at=timezone.now(),
            locked_until=None,
            last_error="",
        )
        published += 1
    return published


def retry_failed_event(*, event_id):
    """Explicitly requeue a failed event after operational review."""
    return PharmacyOutboxEvent.objects.filter(
        event_id=event_id, status=PharmacyOutboxEvent.Status.FAILED
    ).update(
        status=PharmacyOutboxEvent.Status.PENDING,
        available_at=timezone.now(),
        locked_until=None,
        last_error="",
    )


def mark_event_published(*, event_id):
    return PharmacyOutboxEvent.objects.filter(
        event_id=event_id, status=PharmacyOutboxEvent.Status.PROCESSING
    ).update(
        status=PharmacyOutboxEvent.Status.PUBLISHED,
        published_at=timezone.now(),
        locked_until=None,
        last_error="",
    )


__all__ = (
    "MAX_EVENT_ATTEMPTS",
    "enqueue_event",
    "publish_pending_events",
    "retry_failed_event",
    "mark_event_published",
)

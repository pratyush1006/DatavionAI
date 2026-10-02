from datetime import timedelta
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from apps.imaging.models import ImagingOutboxEvent

MAX_EVENT_ATTEMPTS = 8
PROCESSING_LEASE_MINUTES = 5
MAX_RETRY_SECONDS = 60


def enqueue_event(
    *,
    tenant_id,
    event_type,
    aggregate_type,
    aggregate_id=None,
    payload=None,
    event_id=None,
):
    return ImagingOutboxEvent.objects.create(
        tenant_id=tenant_id,
        event_id=event_id or uuid4(),
        event_type=str(event_type),
        aggregate_type=str(aggregate_type),
        aggregate_id=aggregate_id,
        payload=payload or {},
    )


def _claim_event(*, now=None):
    now = now or timezone.now()
    with transaction.atomic():
        event = (
            ImagingOutboxEvent.objects.select_for_update()
            .filter(status=ImagingOutboxEvent.Status.PENDING, available_at__lte=now)
            .order_by("available_at", "created_at")
            .first()
        )
        if event is None:
            event = (
                ImagingOutboxEvent.objects.select_for_update()
                .filter(
                    status=ImagingOutboxEvent.Status.PROCESSING, locked_until__lte=now
                )
                .order_by("available_at", "created_at")
                .first()
            )
        if event is None:
            return None
        event.status = ImagingOutboxEvent.Status.PROCESSING
        event.attempts += 1
        event.locked_until = now + timedelta(minutes=PROCESSING_LEASE_MINUTES)
        event.save(update_fields=("status", "attempts", "locked_until", "updated_at"))
        return event


def publish_pending_events(*, limit=100, publisher=None, now=None):
    if limit <= 0:
        return 0
    if publisher is None:

        def publisher(_):
            raise RuntimeError("No Imaging event publisher is configured.")

    count = 0
    for _ in range(int(limit)):
        event = _claim_event(now=now)
        if event is None:
            break
        try:
            publisher(
                {
                    "event_id": str(event.event_id),
                    "event_type": event.event_type,
                    "aggregate_type": event.aggregate_type,
                    "aggregate_id": (
                        str(event.aggregate_id) if event.aggregate_id else None
                    ),
                    "tenant_id": str(event.tenant_id),
                    "payload": event.payload,
                }
            )
        except Exception as exc:
            if event.attempts >= MAX_EVENT_ATTEMPTS:
                ImagingOutboxEvent.objects.filter(pk=event.pk).update(
                    status=ImagingOutboxEvent.Status.FAILED,
                    locked_until=None,
                    last_error=str(exc)[:4000],
                )
            else:
                ImagingOutboxEvent.objects.filter(pk=event.pk).update(
                    status=ImagingOutboxEvent.Status.PENDING,
                    available_at=timezone.now()
                    + timedelta(
                        seconds=min(MAX_RETRY_SECONDS, 2 ** min(event.attempts, 6))
                    ),
                    locked_until=None,
                    last_error=str(exc)[:4000],
                )
            continue
        ImagingOutboxEvent.objects.filter(pk=event.pk).update(
            status=ImagingOutboxEvent.Status.PUBLISHED,
            published_at=timezone.now(),
            locked_until=None,
            last_error="",
        )
        count += 1
    return count


def retry_failed_event(*, event_id):
    return ImagingOutboxEvent.objects.filter(
        event_id=event_id, status=ImagingOutboxEvent.Status.FAILED
    ).update(
        status=ImagingOutboxEvent.Status.PENDING,
        attempts=0,
        available_at=timezone.now(),
        locked_until=None,
        last_error="",
    )

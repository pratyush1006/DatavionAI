from __future__ import annotations

from datetime import timedelta
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from apps.clinical.medications.models import MedicationOutboxEvent


def enqueue_event(
    *,
    organization,
    event_type,
    aggregate_type,
    aggregate_id=None,
    payload=None,
    event_id=None,
):
    return MedicationOutboxEvent.objects.create(
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
        event = (
            MedicationOutboxEvent.objects.select_for_update()
            .filter(status=MedicationOutboxEvent.Status.PENDING, available_at__lte=now)
            .order_by("available_at", "created_at")
            .first()
        )
        if event is None:
            event = (
                MedicationOutboxEvent.objects.select_for_update()
                .filter(
                    status=MedicationOutboxEvent.Status.PROCESSING,
                    locked_until__lte=now,
                )
                .order_by("available_at", "created_at")
                .first()
            )
        if event is None:
            return None
        event.status = MedicationOutboxEvent.Status.PROCESSING
        event.attempts += 1
        event.locked_until = now + timedelta(minutes=5)
        event.save(update_fields=("status", "attempts", "locked_until", "updated_at"))
        return event


def publish_pending_events(*, limit=100, publisher=None, now=None):
    if limit <= 0:
        return 0
    published = 0
    for _ in range(int(limit)):
        event = _claim_event(now=now)
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
            if publisher is None:
                raise RuntimeError("No Medication event publisher is configured.")
            publisher(envelope)
        except Exception as exc:
            event.status = (
                MedicationOutboxEvent.Status.FAILED
                if event.attempts >= 5
                else MedicationOutboxEvent.Status.PENDING
            )
            event.last_error = str(exc)[:4000]
            event.locked_until = None
            event.available_at = timezone.now() + timedelta(
                minutes=min(60, 2**event.attempts)
            )
            event.save(
                update_fields=(
                    "status",
                    "last_error",
                    "locked_until",
                    "available_at",
                    "updated_at",
                )
            )
            continue
        event.status = MedicationOutboxEvent.Status.PUBLISHED
        event.published_at = timezone.now()
        event.locked_until = None
        event.save(
            update_fields=("status", "published_at", "locked_until", "updated_at")
        )
        published += 1
    return published

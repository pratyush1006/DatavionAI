from __future__ import annotations

from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.notes.models import NoteOutboxEvent


def enqueue_event(*, organization, event_type, aggregate_type, aggregate_id, payload):
    return NoteOutboxEvent.objects.create(
        organization=organization,
        event_type=event_type,
        aggregate_type=aggregate_type,
        aggregate_id=str(aggregate_id),
        payload=payload,
    )


def enqueue_after_commit(**kwargs):
    transaction.on_commit(lambda: enqueue_event(**kwargs))


def claim_event(event_id):
    with transaction.atomic():
        event = NoteOutboxEvent.objects.select_for_update().get(pk=event_id)
        if event.status != "pending" or event.available_at > timezone.now():
            return None
        event.status = "processing"
        event.attempts += 1
        event.save(update_fields=("status", "attempts"))
        return event


def mark_published(event_id):
    return NoteOutboxEvent.objects.filter(pk=event_id).update(
        status="published", published_at=timezone.now()
    )


def mark_failed(event_id, error, retry_seconds=60):
    return NoteOutboxEvent.objects.filter(pk=event_id).update(
        status="pending",
        last_error=str(error)[:4000],
        available_at=timezone.now() + timedelta(seconds=retry_seconds),
    )

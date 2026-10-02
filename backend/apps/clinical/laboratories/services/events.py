from datetime import timedelta
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from ..models import LaboratoryOutboxEvent

MAX_EVENT_ATTEMPTS = 8
PROCESSING_LEASE_MINUTES = 5
MAX_RETRY_SECONDS = 60


def event(org, event_type, entity, entity_id, payload=None):
    return LaboratoryOutboxEvent.objects.create(
        organization_id=org,
        event_id=uuid4(),
        event_type=event_type,
        aggregate_type=entity,
        aggregate_id=entity_id,
        payload=payload or {},
        available_at=timezone.now(),
    )


def _claim_event(*, organization_id=None, now=None):
    now = now or timezone.now()
    with transaction.atomic():
        pending = LaboratoryOutboxEvent.objects.select_for_update().filter(
            status=LaboratoryOutboxEvent.Status.PENDING,
            available_at__lte=now,
        )
        expired = LaboratoryOutboxEvent.objects.select_for_update().filter(
            status=LaboratoryOutboxEvent.Status.PROCESSING,
            locked_until__lte=now,
        )
        if organization_id is not None:
            pending = pending.filter(organization_id=organization_id)
            expired = expired.filter(organization_id=organization_id)
        obj = (pending | expired).order_by("available_at", "created_at").first()
        if obj is None:
            return None
        obj.status = LaboratoryOutboxEvent.Status.PROCESSING
        obj.attempts += 1
        obj.locked_until = now + timedelta(minutes=PROCESSING_LEASE_MINUTES)
        obj.save(update_fields=["status", "attempts", "locked_until", "updated_at"])
        return obj


def publish_pending_events(
    *, limit=100, publisher=None, now=None, organization_id=None
):
    if limit <= 0:
        return 0
    if publisher is None:
        raise RuntimeError("No Laboratory event publisher is configured.")
    published = 0
    for _ in range(int(limit)):
        obj = _claim_event(organization_id=organization_id, now=now)
        if obj is None:
            break
        envelope = {
            "event_id": str(obj.event_id),
            "event_type": obj.event_type,
            "aggregate_type": obj.aggregate_type,
            "aggregate_id": str(obj.aggregate_id) if obj.aggregate_id else None,
            "organization_id": str(obj.organization_id),
            "payload": obj.payload,
        }
        try:
            publisher(envelope)
        except Exception as exc:
            status = (
                LaboratoryOutboxEvent.Status.FAILED
                if obj.attempts >= MAX_EVENT_ATTEMPTS
                else LaboratoryOutboxEvent.Status.PENDING
            )
            delay = min(MAX_RETRY_SECONDS, 2 ** min(obj.attempts, 6))
            LaboratoryOutboxEvent.objects.filter(pk=obj.pk).update(
                status=status,
                available_at=timezone.now() + timedelta(seconds=delay),
                locked_until=None,
                last_error=str(exc)[:4000],
            )
            continue
        LaboratoryOutboxEvent.objects.filter(pk=obj.pk).update(
            status=LaboratoryOutboxEvent.Status.PUBLISHED,
            published_at=timezone.now(),
            locked_until=None,
            last_error="",
        )
        published += 1
    return published


def retry_failed_event(*, event_id, organization_id=None):
    qs = LaboratoryOutboxEvent.objects.filter(
        event_id=event_id,
        status=LaboratoryOutboxEvent.Status.FAILED,
    )
    if organization_id is not None:
        qs = qs.filter(organization_id=organization_id)
    return qs.update(
        status=LaboratoryOutboxEvent.Status.PENDING,
        available_at=timezone.now(),
        locked_until=None,
        last_error="",
    )


def mark_event_published(*, event_id, organization_id=None):
    qs = LaboratoryOutboxEvent.objects.filter(
        event_id=event_id,
        status=LaboratoryOutboxEvent.Status.PROCESSING,
    )
    if organization_id is not None:
        qs = qs.filter(organization_id=organization_id)
    return qs.update(
        status=LaboratoryOutboxEvent.Status.PUBLISHED,
        published_at=timezone.now(),
        locked_until=None,
        last_error="",
    )


def laboratory_readiness(*, organization_id=None):
    from django.db import connection

    checks = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = {"status": "ok"}
    except Exception as exc:
        checks["database"] = {"status": "error", "detail": str(exc)[:500]}
    qs = LaboratoryOutboxEvent.objects.all()
    if organization_id is not None:
        qs = qs.filter(organization_id=organization_id)
    failed = qs.filter(status=LaboratoryOutboxEvent.Status.FAILED).count()
    pending = qs.filter(status=LaboratoryOutboxEvent.Status.PENDING).count()
    checks["outbox"] = {
        "status": "error" if failed else "ok",
        "pending": pending,
        "failed": failed,
    }
    return {
        "status": (
            "ready" if all(v["status"] == "ok" for v in checks.values()) else "degraded"
        ),
        "checks": checks,
    }

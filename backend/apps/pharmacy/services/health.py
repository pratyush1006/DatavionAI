from django.db import connection
from django.utils import timezone

from apps.pharmacy.models import PharmacyOutboxEvent


def pharmacy_health(
    *, organization=None, outbox_warning_threshold=1000, outbox_failure_threshold=1
):
    """Return a deterministic application health/readiness payload."""
    checks = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = {"status": "ok"}
    except Exception as exc:
        checks["database"] = {"status": "error", "detail": str(exc)[:500]}

    qs = PharmacyOutboxEvent.objects.all()
    if organization is not None:
        qs = qs.filter(organization=organization)
    pending = qs.filter(status=PharmacyOutboxEvent.Status.PENDING).count()
    processing = qs.filter(status=PharmacyOutboxEvent.Status.PROCESSING).count()
    failed = qs.filter(status=PharmacyOutboxEvent.Status.FAILED).count()
    checks["outbox"] = {
        "status": (
            "error"
            if failed >= outbox_failure_threshold
            else ("warning" if pending >= outbox_warning_threshold else "ok")
        ),
        "pending": pending,
        "processing": processing,
        "failed": failed,
    }
    healthy = all(item["status"] == "ok" for item in checks.values())
    return {
        "status": "ok" if healthy else "degraded",
        "timestamp": timezone.now().isoformat(),
        "checks": checks,
    }

from django.db.models import Count
from django.utils import timezone

from apps.pharmacy.models import PharmacyOutboxEvent


def outbox_summary(*, organization=None):
    qs = PharmacyOutboxEvent.objects.all()
    if organization is not None:
        qs = qs.filter(organization=organization)
    counts = dict(qs.values_list("status").annotate(count=Count("id")))
    pending = qs.filter(
        status=PharmacyOutboxEvent.Status.PENDING,
        available_at__lte=timezone.now(),
    ).count()
    processing = qs.filter(
        status=PharmacyOutboxEvent.Status.PROCESSING,
        locked_until__lte=timezone.now(),
    ).count()
    return {
        "pending": counts.get(PharmacyOutboxEvent.Status.PENDING, 0),
        "processing": counts.get(PharmacyOutboxEvent.Status.PROCESSING, 0),
        "published": counts.get(PharmacyOutboxEvent.Status.PUBLISHED, 0),
        "failed": counts.get(PharmacyOutboxEvent.Status.FAILED, 0),
        "ready_pending": pending,
        "expired_processing_leases": processing,
    }

from django.db.models import Count
from django.utils import timezone

from ..models import LaboratoryOutboxEvent


def outbox_summary(*, organization_id=None):
    qs = LaboratoryOutboxEvent.objects.all()
    if organization_id is not None:
        qs = qs.filter(organization_id=organization_id)
    counts = dict(qs.values_list("status").annotate(count=Count("id")))
    return {
        "pending": counts.get(LaboratoryOutboxEvent.Status.PENDING, 0),
        "processing": counts.get(LaboratoryOutboxEvent.Status.PROCESSING, 0),
        "published": counts.get(LaboratoryOutboxEvent.Status.PUBLISHED, 0),
        "failed": counts.get(LaboratoryOutboxEvent.Status.FAILED, 0),
        "ready_pending": qs.filter(
            status=LaboratoryOutboxEvent.Status.PENDING,
            available_at__lte=timezone.now(),
        ).count(),
        "expired_processing_leases": qs.filter(
            status=LaboratoryOutboxEvent.Status.PROCESSING,
            locked_until__lte=timezone.now(),
        ).count(),
    }

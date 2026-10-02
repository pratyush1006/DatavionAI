from django.db.models import Count

from apps.imaging.models import ImagingOutboxEvent


def outbox_summary(*, tenant_id):
    return {
        r["status"]: r["count"]
        for r in ImagingOutboxEvent.objects.filter(tenant_id=tenant_id)
        .values("status")
        .annotate(count=Count("id"))
    }

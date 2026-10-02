from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel


class PharmacyOutboxEvent(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PUBLISHED = "published", "Published"
        FAILED = "failed", "Failed"

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_outbox_events",
    )
    event_id = models.UUIDField(unique=True, db_index=True)
    event_type = models.CharField(max_length=120)
    aggregate_type = models.CharField(max_length=100)
    aggregate_id = models.UUIDField(null=True, blank=True)
    payload = models.JSONField(default=dict)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    attempts = models.PositiveIntegerField(default=0)
    available_at = models.DateTimeField(default=timezone.now)
    locked_until = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)

    class Meta:
        db_table = "pharmacy_outbox_events"
        indexes = [
            models.Index(fields=("status", "available_at")),
            models.Index(fields=("organization", "status")),
            models.Index(fields=("aggregate_type", "aggregate_id")),
        ]

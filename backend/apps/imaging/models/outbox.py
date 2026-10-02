import uuid

from django.db import models
from django.utils import timezone


class ImagingOutboxEvent(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PUBLISHED = "published", "Published"
        FAILED = "failed", "Failed"

    id = models.BigAutoField(primary_key=True)
    tenant_id = models.UUIDField(db_index=True)
    event_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    event_type = models.CharField(max_length=160)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "imaging_outbox_events"
        indexes = [
            models.Index(fields=("status", "available_at")),
            models.Index(fields=("tenant_id", "status")),
            models.Index(fields=("aggregate_type", "aggregate_id")),
        ]

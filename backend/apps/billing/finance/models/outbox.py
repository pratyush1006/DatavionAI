import uuid

from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class FinanceOutboxEvent(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PUBLISHED = "published", "Published"
        FAILED = "failed", "Failed"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="finance_core_outbox_events",
    )
    event_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    event_type = models.CharField(max_length=160)
    aggregate_type = models.CharField(max_length=120)
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
        db_table = "finance_core_outbox_events"

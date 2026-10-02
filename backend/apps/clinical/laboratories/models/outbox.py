import uuid

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class LaboratoryOutboxEvent(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="laboratory_outbox_events"
    )
    event_type = models.CharField(max_length=128)
    aggregate_type = models.CharField(max_length=128)
    aggregate_id = models.UUIDField()
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, default="pending")
    attempts = models.PositiveIntegerField(default=0)
    available_at = models.DateTimeField()
    locked_until = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    event_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PUBLISHED = "published", "Published"
        FAILED = "failed", "Failed"


__all__ = (
    "Laboratory",
    "LaboratoryDepartment",
    "LaboratoryTest",
    "LaboratoryPanelItem",
    "LaboratorySlot",
    "LaboratoryOrder",
    "LaboratoryOrderItem",
    "LaboratorySpecimen",
    "LaboratoryResult",
    "LaboratoryReport",
    "LaboratoryAuditLog",
    "LaboratoryOutboxEvent",
)

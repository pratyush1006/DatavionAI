from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class LaboratoryAuditLog(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="laboratory_audit_logs"
    )
    actor_id = models.UUIDField(null=True, blank=True)
    action = models.CharField(max_length=128)
    entity_type = models.CharField(max_length=128)
    entity_id = models.UUIDField()
    metadata = models.JSONField(default=dict, blank=True)

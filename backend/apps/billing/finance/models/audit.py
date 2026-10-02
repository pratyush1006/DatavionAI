from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class FinanceAuditLog(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_core_audit_logs"
    )
    workflow = models.CharField(max_length=160)
    entity_type = models.CharField(max_length=120)
    entity_id = models.UUIDField(null=True, blank=True)
    actor_id = models.UUIDField(null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "finance_core_audit_logs"

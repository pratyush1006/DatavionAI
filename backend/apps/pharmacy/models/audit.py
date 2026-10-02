from django.db import models

from apps.core.models import BaseModel


class PharmacyAuditLog(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="pharmacy_audit_logs",
    )
    action = models.CharField(max_length=80)
    entity_type = models.CharField(max_length=100)
    entity_id = models.UUIDField(null=True, blank=True)
    actor_id = models.UUIDField(null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "pharmacy_audit_logs"
        indexes = [
            models.Index(fields=("organization", "entity_type", "entity_id")),
            models.Index(fields=("organization", "action")),
        ]

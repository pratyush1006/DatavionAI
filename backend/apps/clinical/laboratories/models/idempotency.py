from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class LaboratoryIdempotencyRecord(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="laboratory_idempotency_records",
    )
    key = models.CharField(max_length=255)
    operation = models.CharField(max_length=128)
    response_payload = models.JSONField(default=dict)
    resource_type = models.CharField(max_length=128, blank=True)
    resource_id = models.UUIDField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "key", "operation"),
                name="uq_lab_idempotency_org_key_op",
            )
        ]

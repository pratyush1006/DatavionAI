from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class FinanceIdempotencyKey(BaseModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="finance_core_idempotency_keys",
    )
    key = models.CharField(max_length=180)
    workflow = models.CharField(max_length=160)
    response = models.JSONField(default=dict)

    class Meta:
        db_table = "finance_core_idempotency_keys"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "key", "workflow"),
                name="finance_idempotency_org_key_workflow_uniq",
            )
        ]

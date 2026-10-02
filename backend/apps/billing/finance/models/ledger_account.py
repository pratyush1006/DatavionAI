from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class LedgerAccount(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_ledger_accounts"
    )
    code = models.CharField(max_length=80)
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="children"
    )
    status = models.CharField(max_length=20, default="active")

    class Meta:
        db_table = "finance_ledger_accounts"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"),
                name="finance_ledger_account_org_code_uniq",
            )
        ]

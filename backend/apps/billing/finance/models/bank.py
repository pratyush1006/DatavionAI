from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class BankAccount(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_bank_accounts"
    )
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=120)
    bank_name = models.CharField(max_length=255)
    currency = models.CharField(max_length=12, default="INR")
    opening_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="active")

    class Meta:
        db_table = "finance_bank_accounts"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "account_number"),
                name="finance_bank_org_account_uniq",
            )
        ]

from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization

from .bank import BankAccount


class CashTransaction(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_cash_transactions"
    )
    bank_account = models.ForeignKey(
        BankAccount, on_delete=models.PROTECT, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    transaction_type = models.CharField(max_length=20)
    transaction_date = models.DateTimeField()
    reference = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "finance_cash_transactions"

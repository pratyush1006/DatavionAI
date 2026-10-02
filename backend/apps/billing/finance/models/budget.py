from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class Budget(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_budgets"
    )
    name = models.CharField(max_length=255)
    fiscal_year = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)
    status = models.CharField(max_length=20, default="draft")

    class Meta:
        db_table = "finance_budgets"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "name", "fiscal_year"),
                name="finance_budget_org_name_year_uniq",
            )
        ]

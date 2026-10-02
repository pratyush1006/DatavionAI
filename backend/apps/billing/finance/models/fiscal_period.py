from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class FiscalPeriod(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_fiscal_periods"
    )
    fiscal_year = models.PositiveIntegerField()
    period = models.PositiveSmallIntegerField()
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=20, default="open")

    class Meta:
        db_table = "finance_fiscal_periods"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "fiscal_year", "period"),
                name="finance_fiscal_period_org_year_num_uniq",
            )
        ]

from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization

from .budget import Budget


class FinancialReport(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_reports"
    )
    budget = models.ForeignKey(
        Budget, on_delete=models.PROTECT, null=True, blank=True, related_name="reports"
    )
    report_type = models.CharField(max_length=80)
    title = models.CharField(max_length=255)
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=20, default="pending")
    generated_at = models.DateTimeField(null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "finance_financial_reports"

from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class TaxRate(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_tax_rates"
    )
    code = models.CharField(max_length=80)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    rate = models.DecimalField(max_digits=8, decimal_places=4)
    tax_type = models.CharField(max_length=80)

    class Meta:
        db_table = "finance_tax_rates"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"), name="finance_tax_rate_org_code_uniq"
            )
        ]


class TaxFiling(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_tax_filings"
    )
    tax_rate = models.ForeignKey(
        TaxRate, on_delete=models.PROTECT, related_name="filings"
    )
    period = models.CharField(max_length=40)
    period_start = models.DateField()
    period_end = models.DateField()
    taxable_amount = models.DecimalField(max_digits=18, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=18, decimal_places=2)
    reference = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=20, default="draft")

    class Meta:
        db_table = "finance_tax_filings"

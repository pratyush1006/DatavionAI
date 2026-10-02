from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class Vendor(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_vendors"
    )
    code = models.CharField(max_length=80)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    tax_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default="active")

    class Meta:
        db_table = "finance_vendors"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"), name="finance_vendor_org_code_uniq"
            )
        ]


class VendorInvoice(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_vendor_invoices"
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.PROTECT, related_name="invoices"
    )
    invoice_number = models.CharField(max_length=100)
    reference = models.CharField(max_length=160, blank=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="draft")

    class Meta:
        db_table = "finance_vendor_invoices"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "invoice_number"),
                name="finance_vendor_invoice_org_number_uniq",
            )
        ]

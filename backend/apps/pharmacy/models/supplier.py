from django.db import models

from apps.core.models import BaseModel


class Supplier(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="pharmacy_suppliers",
    )
    code = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    tax_id = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        db_table = "pharmacy_suppliers"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"),
                name="unique_pharmacy_supplier_code_per_org",
            )
        ]
        ordering = ("name",)

    def __str__(self):
        return f"{self.code} | {self.name}"

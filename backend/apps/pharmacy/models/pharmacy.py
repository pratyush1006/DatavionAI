from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import PharmacyStatus


class Pharmacy(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="pharmacies",
    )
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(
        max_length=20, choices=PharmacyStatus.choices, default=PharmacyStatus.ACTIVE
    )

    class Meta:
        db_table = "pharmacies"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"),
                name="unique_pharmacy_code_per_organization",
            )
        ]
        ordering = ("name",)

    def __str__(self):
        return f"{self.code} | {self.name}"

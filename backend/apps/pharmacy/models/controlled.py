from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import ControlledSubstanceSchedule
from apps.pharmacy.models.product import PharmacyProduct


class ControlledSubstanceControl(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_controlled_substances",
    )
    product = models.OneToOneField(
        PharmacyProduct, on_delete=models.PROTECT, related_name="controlled_control"
    )
    schedule = models.CharField(
        max_length=20, choices=ControlledSubstanceSchedule.choices
    )
    requires_double_check = models.BooleanField(default=True)
    max_daily_quantity = models.DecimalField(
        max_digits=14, decimal_places=3, null=True, blank=True
    )
    license_reference = models.CharField(max_length=120, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "pharmacy_controlled_substance_controls"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "product"),
                name="unique_controlled_control_per_org_product",
            )
        ]

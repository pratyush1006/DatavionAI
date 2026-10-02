from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization

from .department import LaboratoryDepartment


class LaboratoryTest(BaseModel):
    objects = BaseManager()
    # Legacy compatibility: existing catalog rows may predate tenant linkage.
    # Organization ownership is required for all new records.
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="laboratory_test_catalog"
    )
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=128, blank=True)
    department = models.ForeignKey(
        LaboratoryDepartment,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="tests",
    )
    specimen_type = models.CharField(max_length=128)
    preparation = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    unit = models.CharField(max_length=64, blank=True)
    reference_range = models.JSONField(default=dict, blank=True)
    critical_range = models.JSONField(default=dict, blank=True)
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    turnaround_minutes = models.PositiveIntegerField(default=0)
    is_panel = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default="active")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"), name="uq_lab_test_org_code"
            )
        ]

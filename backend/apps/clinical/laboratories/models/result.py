from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization

from .order import LaboratoryOrderItem


class LaboratoryResult(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="laboratory_results"
    )
    order_item = models.OneToOneField(
        LaboratoryOrderItem, on_delete=models.PROTECT, related_name="result"
    )
    status = models.CharField(max_length=30, default="pending")
    value_numeric = models.DecimalField(
        max_digits=18, decimal_places=6, null=True, blank=True
    )
    value_text = models.TextField(blank=True)
    unit = models.CharField(max_length=64, blank=True)
    reference_range = models.JSONField(default=dict, blank=True)
    abnormal_flag = models.CharField(max_length=30, default="normal")
    critical = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    entered_by_id = models.UUIDField(null=True, blank=True)
    verified_by_id = models.UUIDField(null=True, blank=True)
    entered_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)

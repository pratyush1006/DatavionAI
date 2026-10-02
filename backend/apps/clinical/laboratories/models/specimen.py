from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization

from .order import LaboratoryOrder


class LaboratorySpecimen(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="laboratory_specimens"
    )
    order = models.ForeignKey(
        LaboratoryOrder, on_delete=models.PROTECT, related_name="specimens"
    )
    specimen_id = models.CharField(max_length=64, unique=True)
    accession_number = models.CharField(max_length=64, unique=True)
    barcode = models.CharField(max_length=128, unique=True)
    specimen_type = models.CharField(max_length=128)
    status = models.CharField(max_length=30, default="expected")
    collected_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    collector_user_id = models.UUIDField(null=True, blank=True)
    chain_of_custody = models.JSONField(default=list, blank=True)

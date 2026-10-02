from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class Laboratory(BaseModel):
    objects = BaseManager()

    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="clinical_laboratories"
    )
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    address = models.JSONField(default=dict, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    status = models.CharField(max_length=20, default="active")
    appointment_enabled = models.BooleanField(default=True)
    home_collection_enabled = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"), name="uq_lab_org_code"
            )
        ]

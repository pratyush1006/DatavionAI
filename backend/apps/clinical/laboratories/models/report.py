from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization

from .order import LaboratoryOrder


class LaboratoryReport(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="laboratory_reports"
    )
    order = models.OneToOneField(
        LaboratoryOrder, on_delete=models.PROTECT, related_name="report"
    )
    report_number = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=30, default="draft")
    title = models.CharField(max_length=255, default="Laboratory Report")
    report_data = models.JSONField(default=dict)
    verified_by_id = models.UUIDField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    pdf_file = models.FileField(upload_to="laboratory/reports/%Y/%m/", blank=True)

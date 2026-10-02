import uuid

from django.db import models


class DeviceConsent(models.Model):
    consent_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="device_consents",
    )
    patient = models.ForeignKey(
        "patient_core.Patient", on_delete=models.PROTECT, related_name="device_consents"
    )
    device = models.ForeignKey(
        "device_platform.Device", on_delete=models.PROTECT, related_name="consents"
    )
    purpose = models.CharField(max_length=120)
    granted = models.BooleanField(default=False)
    granted_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_platform_consents"
        indexes = [
            models.Index(
                fields=["organization", "patient", "device"],
                name="dp_consent_org_pat_dev_idx",
            ),
        ]

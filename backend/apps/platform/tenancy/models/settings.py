"""
Tenant settings model.

Stores configurable tenant-level preferences
and feature configuration.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.platform.tenancy.models.tenant import Tenant


class TenantSettings(BaseModel):
    """
    Configuration container for a tenant.
    """

    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name="settings_config",
    )

    timezone = models.CharField(
        max_length=100,
        default="UTC",
    )

    language = models.CharField(
        max_length=20,
        default="en",
    )

    currency = models.CharField(
        max_length=10,
        default="INR",
    )

    feature_flags = models.JSONField(
        default=dict,
        blank=True,
    )

    preferences = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        db_table = "platform_tenant_settings"

    def __str__(self) -> str:
        return f"{self.tenant.name} Settings"

"""
Tenant domain model.

Maps domains/subdomains to DatavionOS tenants.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.platform.tenancy.models.tenant import Tenant


class TenantDomain(BaseModel):
    """
    Domain mapping for tenant resolution.
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="domains",
    )

    domain = models.CharField(
        max_length=255,
        unique=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "platform_tenant_domains"
        ordering = ("domain",)

    def __str__(self) -> str:
        return self.domain

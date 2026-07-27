"""
Tenant model.

Represents SaaS isolation boundary in DatavionOS.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.platform.tenancy.constants import (
    TenantStatus,
    TenantType,
)
from apps.platform.tenancy.managers import (
    TenantManager,
)


class Tenant(BaseModel):
    """
    Root SaaS tenant.

    Every business entity belongs to a tenant.
    """

    objects = TenantManager()

    name = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    tenant_type = models.CharField(
        max_length=50,
        choices=TenantType.choices,
        default=TenantType.CLINIC,
    )

    status = models.CharField(
        max_length=50,
        choices=TenantStatus.choices,
        default=TenantStatus.ACTIVE,
    )

    class Meta:
        db_table = "platform_tenants"

        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

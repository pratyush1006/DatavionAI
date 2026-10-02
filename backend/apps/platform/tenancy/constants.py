"""
Tenant constants for DatavionOS SaaS platform.
"""

from __future__ import annotations

from django.db.models import TextChoices


class TenantStatus(TextChoices):
    """
    Tenant lifecycle states.
    """

    ACTIVE = "active", "Active"

    INACTIVE = "inactive", "Inactive"

    SUSPENDED = "suspended", "Suspended"

    DELETED = "deleted", "Deleted"


class TenantType(TextChoices):
    """
    Tenant categories.
    """

    CLINIC = "clinic", "Clinic"

    HOSPITAL = "hospital", "Hospital"

    LABORATORY = "laboratory", "Laboratory"

    PHARMACY = "pharmacy", "Pharmacy"

    ENTERPRISE = "enterprise", "Enterprise"

"""
Constants for the Patient Portal bounded context.
"""

from __future__ import annotations

from django.db import models


class PortalAccountStatus(models.TextChoices):
    """Lifecycle states for a patient portal account."""

    INVITED = "INVITED", "Invited"
    ACTIVE = "ACTIVE", "Active"
    SUSPENDED = "SUSPENDED", "Suspended"
    LOCKED = "LOCKED", "Locked"
    DEACTIVATED = "DEACTIVATED", "Deactivated"


class PortalAuthProvider(models.TextChoices):
    """Supported authentication provider categories."""

    LOCAL = "LOCAL", "Local"
    GOOGLE = "GOOGLE", "Google"
    MICROSOFT = "MICROSOFT", "Microsoft"
    SSO = "SSO", "Single Sign-On"


ALLOWED_STATUS_TRANSITIONS = {
    PortalAccountStatus.INVITED: {
        PortalAccountStatus.ACTIVE,
        PortalAccountStatus.DEACTIVATED,
    },
    PortalAccountStatus.ACTIVE: {
        PortalAccountStatus.SUSPENDED,
        PortalAccountStatus.LOCKED,
        PortalAccountStatus.DEACTIVATED,
    },
    PortalAccountStatus.SUSPENDED: {
        PortalAccountStatus.ACTIVE,
        PortalAccountStatus.DEACTIVATED,
    },
    PortalAccountStatus.LOCKED: {
        PortalAccountStatus.ACTIVE,
        PortalAccountStatus.DEACTIVATED,
    },
    PortalAccountStatus.DEACTIVATED: set(),
}


__all__ = (
    "ALLOWED_STATUS_TRANSITIONS",
    "PortalAccountStatus",
    "PortalAuthProvider",
)

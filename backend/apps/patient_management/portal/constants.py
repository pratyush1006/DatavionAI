"""
Constants for the Patient Portal module.
"""

from __future__ import annotations

from django.db import models


class PortalAccountStatus(models.TextChoices):
    """
    Patient portal account status.
    """

    INVITED = "invited", "Invited"

    ACTIVE = "active", "Active"

    SUSPENDED = "suspended", "Suspended"

    DEACTIVATED = "deactivated", "Deactivated"


class PortalAuthProvider(models.TextChoices):
    """
    Authentication provider for the portal.
    """

    LOCAL = "local", "Local"

    GOOGLE = "google", "Google"

    APPLE = "apple", "Apple"

    OTP = "otp", "OTP"


__all__ = [
    "PortalAccountStatus",
    "PortalAuthProvider",
]

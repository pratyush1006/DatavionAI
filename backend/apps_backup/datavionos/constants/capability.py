"""
Capability constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class CapabilityCategory(TextChoices):
    """
    Supported capability categories.
    """

    CLINICAL = "clinical", "Clinical"
    FINANCIAL = "financial", "Financial"
    OPERATIONS = "operations", "Operations"
    INTEGRATION = "integration", "Integration"
    AI = "ai", "AI"
    PLATFORM = "platform", "Platform"


class CapabilityStatus(TextChoices):
    """
    Supported capability statuses.
    """

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DEPRECATED = "deprecated", "Deprecated"


class ModuleCategory(TextChoices):
    """
    Supported module categories.
    """

    CORE = "core", "Core"
    CLINICAL = "clinical", "Clinical"
    FINANCIAL = "financial", "Financial"
    INTEGRATION = "integration", "Integration"
    AI = "ai", "AI"
    UTILITY = "utility", "Utility"


class ModuleStatus(TextChoices):
    """
    Supported module statuses.
    """

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DEPRECATED = "deprecated", "Deprecated"


class PluginStatus(TextChoices):
    """
    Supported plugin statuses.
    """

    ACTIVE = "active", "Active"
    REGISTERED = "registered", "Registered"
    LOADED = "loaded", "Loaded"
    ENABLED = "enabled", "Enabled"
    DISABLED = "disabled", "Disabled"
    FAILED = "failed", "Failed"


class ServiceLifetime(TextChoices):
    """
    Supported service lifetimes.
    """

    SINGLETON = "singleton", "Singleton"
    SCOPED = "scoped", "Scoped"
    TRANSIENT = "transient", "Transient"


class ServiceStatus(TextChoices):
    """
    Supported service statuses.
    """

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DEPRECATED = "deprecated", "Deprecated"


__all__ = [
    "CapabilityCategory",
    "CapabilityStatus",
    "ModuleCategory",
    "ModuleStatus",
    "PluginStatus",
    "ServiceLifetime",
    "ServiceStatus",
]

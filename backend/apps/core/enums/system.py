"""System-level enumerations for the DatavionOS platform."""

from __future__ import annotations

from enum import StrEnum

from .tenant import TenantStatus, TenantType


class DeploymentMode(StrEnum):
    """Supported application deployment environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class ServiceStatus(StrEnum):
    """Lifecycle states for registered platform services."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"


__all__ = ["DeploymentMode", "ServiceStatus", "TenantStatus", "TenantType"]

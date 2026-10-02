"""
Platform-wide enumerations for the DatavionOS platform.

This package provides shared enumerations used throughout the
platform to improve consistency, readability, and type safety.
"""

from __future__ import annotations

# ============================================================================
# Audit
# ============================================================================
from .audit import (
    AuditAction,
    AuditCategory,
    AuditOutcome,
    AuditSeverity,
)

# ============================================================================
# Environment
# ============================================================================
from .environment import (
    Environment,
)

# ============================================================================
# HTTP
# ============================================================================
from .http import (
    HTTPHeader,
    HTTPMethod,
)

# ============================================================================
# Status
# ============================================================================
from .status import (
    HealthStatus,
    OperationStatus,
    ResourceStatus,
)

# ============================================================================
# System
# ============================================================================
from .system import (
    DeploymentMode,
    ServiceStatus,
)

# ============================================================================
# Tenant
# ============================================================================
from .tenant import (
    TenantStatus,
    TenantType,
)

__all__ = [
    # Audit
    "AuditAction",
    "AuditCategory",
    "AuditOutcome",
    "AuditSeverity",
    # Environment
    "Environment",
    # HTTP
    "HTTPHeader",
    "HTTPMethod",
    # Status
    "HealthStatus",
    "OperationStatus",
    "ResourceStatus",
    # System
    "DeploymentMode",
    "ServiceStatus",
    # Tenant
    "TenantStatus",
    "TenantType",
]

"""
Common type aliases for the DatavionOS kernel.

This module defines the canonical type aliases shared throughout the
DatavionOS kernel. These aliases improve readability, provide semantic
meaning, and ensure consistent typing across contracts, runtime services,
plugins, events, workflows, and integrations.

The aliases defined here are intentionally lightweight and should remain
free of framework-specific dependencies.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    NewType,
    TypeAlias,
)

# ============================================================================
# Identifier Types
# ============================================================================

Identifier = NewType("Identifier", str)

TenantIdentifier = NewType("TenantIdentifier", str)

WorkspaceIdentifier = NewType("WorkspaceIdentifier", str)

UserIdentifier = NewType("UserIdentifier", str)

PluginName = NewType("PluginName", str)

CapabilityName = NewType("CapabilityName", str)

PermissionName = NewType("PermissionName", str)

FeatureFlag = NewType("FeatureFlag", str)

# ============================================================================
# Collection Types
# ============================================================================

Metadata: TypeAlias = dict[str, Any]

Context: TypeAlias = dict[str, Any]

Properties: TypeAlias = dict[str, Any]

Labels: TypeAlias = dict[str, str]

TagSet: TypeAlias = set[str]

ReadonlyMetadata: TypeAlias = Mapping[str, Any]

ReadonlyContext: TypeAlias = Mapping[str, Any]

# ============================================================================
# Common Literal Types
# ============================================================================

Environment: TypeAlias = Literal[
    "development",
    "testing",
    "staging",
    "production",
]

LifecycleState: TypeAlias = Literal[
    "registered",
    "initialized",
    "starting",
    "running",
    "stopping",
    "stopped",
    "failed",
]

PluginStatus: TypeAlias = Literal[
    "discovered",
    "registered",
    "loaded",
    "enabled",
    "disabled",
    "failed",
]

CapabilityStatus: TypeAlias = Literal[
    "enabled",
    "disabled",
]

# ============================================================================
# Public Exports
# ============================================================================

__all__ = [
    "CapabilityName",
    "CapabilityStatus",
    "Context",
    "Environment",
    "FeatureFlag",
    "Identifier",
    "Labels",
    "LifecycleState",
    "Metadata",
    "PermissionName",
    "PluginName",
    "PluginStatus",
    "Properties",
    "ReadonlyContext",
    "ReadonlyMetadata",
    "TagSet",
    "TenantIdentifier",
    "UserIdentifier",
    "WorkspaceIdentifier",
]

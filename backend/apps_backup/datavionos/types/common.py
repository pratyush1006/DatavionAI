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

type Metadata = dict[str, Any]

type Context = dict[str, Any]

type Properties = dict[str, Any]

type Labels = dict[str, str]

type TagSet = set[str]

type ReadonlyMetadata = Mapping[str, Any]

type ReadonlyContext = Mapping[str, Any]

# ============================================================================
# Common Literal Types
# ============================================================================

type Environment = Literal[
    "development",
    "testing",
    "staging",
    "production",
]

type LifecycleState = Literal[
    "registered",
    "initialized",
    "starting",
    "running",
    "stopping",
    "stopped",
    "failed",
]

type PluginStatus = Literal[
    "discovered",
    "registered",
    "loaded",
    "enabled",
    "disabled",
    "failed",
]

type CapabilityStatus = Literal[
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

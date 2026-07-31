"""
Public type aliases for the DatavionOS kernel.

The ``types`` package contains reusable type aliases shared across the
DatavionOS kernel. These aliases improve readability, encourage consistency,
and provide a stable public typing API for plugins, runtime components,
contracts, and integrations.

Type aliases must remain:

- Lightweight
- Framework agnostic
- Free of runtime side effects
- Backward compatible whenever possible

Consumers should always import types from this package rather than individual
implementation modules.
"""

from __future__ import annotations

from apps.datavionos.types.common import (
    CapabilityName,
    Context,
    FeatureFlag,
    Identifier,
    Labels,
    Metadata,
    PermissionName,
    PluginName,
    Properties,
    TagSet,
    TenantIdentifier,
    UserIdentifier,
    WorkspaceIdentifier,
)

__all__ = [
    "CapabilityName",
    "Context",
    "FeatureFlag",
    "Identifier",
    "Labels",
    "Metadata",
    "PermissionName",
    "PluginName",
    "Properties",
    "TagSet",
    "TenantIdentifier",
    "UserIdentifier",
    "WorkspaceIdentifier",
]

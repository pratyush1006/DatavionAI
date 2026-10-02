"""Device Platform integration with canonical DatavionAI RBAC."""

from __future__ import annotations

from apps.platform.rbac.resolvers import resolve_permissions

DEVICE_PERMISSIONS = (
    "device_platform.view",
    "device_platform.manage",
    "device_platform.pair",
    "device_platform.associate",
    "device_platform.telemetry_ingest",
    "device_platform.telemetry_view",
)


def has_device_permission(user, code: str, organization=None) -> bool:
    if not user or not getattr(user, "is_authenticated", False):
        return False
    if not code:
        return False
    permissions = resolve_permissions(user=user, organization=organization)
    return code in permissions


__all__ = ["DEVICE_PERMISSIONS", "has_device_permission"]

"""
DatavionOS permission registry.

Defines platform-level permission contracts used by RBAC.

The registry provides permission discovery for:

- Roles
- Users
- Organizations
- Modules
- Subscription capabilities
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import Registry


@dataclass(
    frozen=True,
    slots=True,
)
class PermissionDefinition:
    """
    Defines a platform permission.

    Examples:

        patient.create

        appointment.book

        laboratory.order
    """

    code: str

    name: str

    description: str

    module: str | None = None

    resource: str | None = None

    action: str | None = None

    category: str = "platform"

    enabled: bool = True

    is_sensitive: bool = False


permission_registry = Registry[PermissionDefinition]()


__all__: tuple[str, ...] = (
    "PermissionDefinition",
    "permission_registry",
)

"""
Built-in RBAC permissions.
"""

from __future__ import annotations

from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)


def build_permissions() -> list[dict[str, object]]:
    """
    Build the default platform permissions.
    """

    permissions: list[dict[str, object]] = []

    display_order = 0

    for module in PermissionModule:
        for action in PermissionAction:
            permissions.append(
                {
                    "name": (f"{action.label} {module.label}"),
                    "code": (f"{module.value}.{action.value}"),
                    "module": module.value,
                    "action": action.value,
                    "scope": (PermissionScope.ORGANIZATION),
                    "description": (
                        f"Allows a user to "
                        f"{action.label.lower()} "
                        f"{module.label.lower()}."
                    ),
                    "display_order": display_order,
                    "is_system": True,
                    "is_assignable": True,
                    "is_delegable": False,
                },
            )

            display_order += 1

    return permissions


PERMISSIONS = build_permissions()


__all__ = [
    "PERMISSIONS",
]

"""
Security context contracts.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.security.identity import Identity
from apps.datavionos.security.permission import Permission
from apps.datavionos.security.policy import Policy
from apps.datavionos.security.principal import Principal
from apps.datavionos.security.role import Role


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityContext:
    """
    Immutable security execution context.
    """

    identity: Identity

    principal: Principal

    roles: frozenset[Role] = frozenset()

    permissions: frozenset[Permission] = frozenset()

    policies: frozenset[Policy] = frozenset()

    @property
    def is_authenticated(
        self,
    ) -> bool:
        """
        Return whether the current identity
        is authenticated.
        """
        return self.identity.is_authenticated

    def has_permission(
        self,
        permission: str,
    ) -> bool:
        """
        Determine whether the context contains
        the specified permission.
        """
        return any(item.name == permission for item in self.permissions)

    def has_role(
        self,
        role_name: str,
    ) -> bool:
        """
        Determine whether the context contains
        the specified role.
        """
        return any(role.name == role_name for role in self.roles)


__all__ = [
    "SecurityContext",
]

"""
Provider RBAC permissions.

Provider bounded context permission adapters.

Uses DatavionOS centralized RBAC engine.

Permission convention:

    providers.<action>

Examples:

    providers.view
    providers.create
    providers.update
    providers.verify
    providers.activate
    providers.deactivate
    providers.assign
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)


class CanViewProvider(
    RBACPermissionBase,
):
    """
    Allows viewing providers.
    """

    message = "You do not have permission to view providers."

    permission_code = "providers.view"


class CanCreateProvider(
    RBACPermissionBase,
):
    """
    Allows creating providers.
    """

    message = "You do not have permission to create providers."

    permission_code = "providers.create"


class CanUpdateProvider(
    RBACPermissionBase,
):
    """
    Allows updating providers.
    """

    message = "You do not have permission to update providers."

    permission_code = "providers.update"


class CanVerifyProvider(
    RBACPermissionBase,
):
    """
    Allows verifying providers.

    Used by:

    - ProviderVerificationWorkflow
    """

    message = "You do not have permission to verify providers."

    permission_code = "providers.verify"


class CanActivateProvider(
    RBACPermissionBase,
):
    """
    Allows activating providers.

    Used by:

    - ProviderActivationWorkflow
    """

    message = "You do not have permission to activate providers."

    permission_code = "providers.activate"


class CanDeactivateProvider(
    RBACPermissionBase,
):
    """
    Allows deactivating providers.

    Used by:

    - ProviderDeactivationWorkflow
    """

    message = "You do not have permission to deactivate providers."

    permission_code = "providers.deactivate"


class CanAssignProvider(
    RBACPermissionBase,
):
    """
    Allows assigning providers.

    Used by:

    - ProviderAssignmentWorkflow
    """

    message = "You do not have permission to assign providers."

    permission_code = "providers.assign"


__all__ = (
    "CanViewProvider",
    "CanCreateProvider",
    "CanUpdateProvider",
    "CanVerifyProvider",
    "CanActivateProvider",
    "CanDeactivateProvider",
    "CanAssignProvider",
)

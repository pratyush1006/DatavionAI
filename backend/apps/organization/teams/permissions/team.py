"""
Team RBAC permissions.

Team bounded context permission adapters.

Uses the DatavionOS centralized RBAC engine.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)


class CanViewTeam(
    RBACPermissionBase,
):
    """
    Allows viewing teams.
    """

    message = "You do not have permission to view teams."

    permission_code = "teams.view"


class CanCreateTeam(
    RBACPermissionBase,
):
    """
    Allows creating teams.
    """

    message = "You do not have permission to create teams."

    permission_code = "teams.create"


class CanUpdateTeam(
    RBACPermissionBase,
):
    """
    Allows updating teams.
    """

    message = "You do not have permission to update teams."

    permission_code = "teams.update"


class CanDeleteTeam(
    RBACPermissionBase,
):
    """
    Allows deleting teams.
    """

    message = "You do not have permission to delete teams."

    permission_code = "teams.delete"


class CanActivateTeam(
    RBACPermissionBase,
):
    """
    Allows activating teams.
    """

    message = "You do not have permission to activate teams."

    permission_code = "teams.activate"


class CanDeactivateTeam(
    RBACPermissionBase,
):
    """
    Allows deactivating teams.
    """

    message = "You do not have permission to deactivate teams."

    permission_code = "teams.deactivate"


class CanAssignTeamMember(
    RBACPermissionBase,
):
    """
    Allows assigning members to teams.
    """

    message = "You do not have permission to assign team members."

    permission_code = "teams.assign"


class CanApproveTeam(
    RBACPermissionBase,
):
    """
    Allows approving team operations.
    """

    message = "You do not have permission to approve team operations."

    permission_code = "teams.approve"


__all__ = (
    "CanViewTeam",
    "CanCreateTeam",
    "CanUpdateTeam",
    "CanDeleteTeam",
    "CanActivateTeam",
    "CanDeactivateTeam",
    "CanAssignTeamMember",
    "CanApproveTeam",
)

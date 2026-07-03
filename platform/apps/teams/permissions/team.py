"""
Team permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import (
    DatavionPermission,
)


class CanViewTeam(DatavionPermission):
    """
    Permission to view teams.
    """

    permission_code = "team.view"


class CanCreateTeam(DatavionPermission):
    """
    Permission to create teams.
    """

    permission_code = "team.create"


class CanUpdateTeam(DatavionPermission):
    """
    Permission to update teams.
    """

    permission_code = "team.update"


class CanDeleteTeam(DatavionPermission):
    """
    Permission to delete teams.
    """

    permission_code = "team.delete"


__all__ = [
    "CanViewTeam",
    "CanCreateTeam",
    "CanUpdateTeam",
    "CanDeleteTeam",
]

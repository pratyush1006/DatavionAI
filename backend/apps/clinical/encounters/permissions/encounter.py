"""
Encounter permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewEncounter(BasePermission):
    """
    Permission required to view encounters.
    """

    permission_code = "encounter.view"


class CanCreateEncounter(BasePermission):
    """
    Permission required to create encounters.
    """

    permission_code = "encounter.create"


class CanUpdateEncounter(BasePermission):
    """
    Permission required to update encounters.
    """

    permission_code = "encounter.update"


class CanDeleteEncounter(BasePermission):
    """
    Permission required to delete encounters.
    """

    permission_code = "encounter.delete"


__all__ = [
    "CanCreateEncounter",
    "CanDeleteEncounter",
    "CanUpdateEncounter",
    "CanViewEncounter",
]

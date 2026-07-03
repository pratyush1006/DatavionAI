"""
Role assignment permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanAssignRole(BasePermission):
    permission_code = "user_role.assign"


class CanRemoveRole(BasePermission):
    permission_code = "user_role.remove"


class CanAssignPermission(BasePermission):
    permission_code = "role_permission.assign"


class CanRemovePermission(BasePermission):
    permission_code = "role_permission.remove"

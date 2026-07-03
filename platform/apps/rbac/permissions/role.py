"""
Role permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewRole(BasePermission):
    permission_code = "role.view"


class CanCreateRole(BasePermission):
    permission_code = "role.create"


class CanUpdateRole(BasePermission):
    permission_code = "role.update"


class CanDeleteRole(BasePermission):
    permission_code = "role.delete"

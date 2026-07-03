"""
Permission permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewPermission(BasePermission):
    permission_code = "permission.view"


class CanCreatePermission(BasePermission):
    permission_code = "permission.create"


class CanUpdatePermission(BasePermission):
    permission_code = "permission.update"


class CanDeletePermission(BasePermission):
    permission_code = "permission.delete"

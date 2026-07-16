"""
Base RBAC permission.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated


class BaseRBACPermission(IsAuthenticated):
    """
    Base permission for all RBAC endpoints.
    """

    permission_code: str | None = None

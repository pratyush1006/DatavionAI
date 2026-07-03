"""
RolePermission filters.
"""

from __future__ import annotations

import django_filters

from apps.rbac.models import RolePermission


class RolePermissionFilter(django_filters.FilterSet):
    """
    FilterSet for RolePermission.
    """

    class Meta:
        model = RolePermission
        fields = (
            "role",
            "permission",
        )

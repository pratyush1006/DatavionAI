"""
UserRole filters.
"""

from __future__ import annotations

import django_filters

from apps.platform.rbac.models import UserRole


class UserRoleFilter(django_filters.FilterSet):
    """
    FilterSet for UserRole.
    """

    class Meta:
        model = UserRole
        fields = (
            "user",
            "role",
        )

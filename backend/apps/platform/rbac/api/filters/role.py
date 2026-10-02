"""
Role filters.
"""

from __future__ import annotations

import django_filters

from apps.platform.rbac.models import Role


class RoleFilter(django_filters.FilterSet):
    """
    FilterSet for Role.
    """

    name = django_filters.CharFilter(lookup_expr="icontains")
    code = django_filters.CharFilter(lookup_expr="icontains")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Role
        fields = (
            "name",
            "code",
            "is_active",
        )

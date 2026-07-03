"""
Permission filters.
"""

from __future__ import annotations

import django_filters

from apps.rbac.models import Permission


class PermissionFilter(django_filters.FilterSet):
    """
    FilterSet for Permission.
    """

    name = django_filters.CharFilter(lookup_expr="icontains")
    code = django_filters.CharFilter(lookup_expr="icontains")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Permission
        fields = (
            "name",
            "code",
            "is_active",
        )

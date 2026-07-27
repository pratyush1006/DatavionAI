"""
Filters for the Emergency Contacts module.
"""

from __future__ import annotations

import django_filters

from ...models import EmergencyContact


class EmergencyContactFilter(
    django_filters.FilterSet,
):
    """
    Emergency contact filter.
    """

    search = django_filters.CharFilter(
        method="filter_search",
    )

    is_primary = django_filters.BooleanFilter()

    is_verified = django_filters.BooleanFilter()

    relationship = django_filters.CharFilter()

    status = django_filters.CharFilter()

    patient = django_filters.UUIDFilter(
        field_name="patient__uuid",
    )

    organization = django_filters.UUIDFilter(
        field_name="organization__uuid",
    )

    class Meta:
        model = EmergencyContact

        fields = (
            "patient",
            "organization",
            "relationship",
            "status",
            "is_primary",
            "is_verified",
        )

    def filter_search(
        self,
        queryset,
        name,
        value,
    ):
        return queryset.search(value)

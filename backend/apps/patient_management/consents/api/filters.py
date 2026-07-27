"""
Filters for the Patient Consents module.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.consents.models import (
    Consent,
)

__all__ = [
    "ConsentFilter",
]


class ConsentFilter(
    django_filters.FilterSet,
):
    """
    Consent filtering.
    """

    created_before = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte",
    )

    created_after = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte",
    )

    effective_before = django_filters.DateFilter(
        field_name="effective_date",
        lookup_expr="lte",
    )

    effective_after = django_filters.DateFilter(
        field_name="effective_date",
        lookup_expr="gte",
    )

    expiry_before = django_filters.DateFilter(
        field_name="expiry_date",
        lookup_expr="lte",
    )

    expiry_after = django_filters.DateFilter(
        field_name="expiry_date",
        lookup_expr="gte",
    )

    search = django_filters.CharFilter(
        method="filter_search",
    )

    class Meta:
        model = Consent

        fields = (
            "organization",
            "patient",
            "consent_type",
            "status",
            "method",
            "source",
            "is_required",
            "is_active",
        )

    def filter_search(
        self,
        queryset,
        name,
        value,
    ):
        return queryset.filter(
            title__icontains=value,
        ) | queryset.filter(
            consent_number__icontains=value,
        )

"""
Filters for listing and querying patient family members.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.family_members.constants import (
    FamilyMemberGender,
    FamilyMemberRelationship,
    FamilyMemberStatus,
)
from apps.patient_management.family_members.models import FamilyMember


class FamilyMemberFilter(django_filters.FilterSet):
    """Filters for tenant-scoped Family Member queries."""

    search = django_filters.CharFilter(method="filter_search")
    patient = django_filters.UUIDFilter(field_name="patient_id")

    relationship = django_filters.ChoiceFilter(
        choices=FamilyMemberRelationship.choices,
    )
    gender = django_filters.ChoiceFilter(
        choices=FamilyMemberGender.choices,
    )
    status = django_filters.ChoiceFilter(
        choices=FamilyMemberStatus.choices,
    )

    is_living = django_filters.BooleanFilter()
    is_next_of_kin = django_filters.BooleanFilter()
    is_emergency_contact = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    created_after = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte",
    )
    created_before = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte",
    )
    updated_after = django_filters.DateFilter(
        field_name="updated_at",
        lookup_expr="date__gte",
    )
    updated_before = django_filters.DateFilter(
        field_name="updated_at",
        lookup_expr="date__lte",
    )

    class Meta:
        model = FamilyMember
        fields = (
            "patient",
            "relationship",
            "gender",
            "status",
            "is_living",
            "is_next_of_kin",
            "is_emergency_contact",
            "is_active",
        )

    @staticmethod
    def filter_search(queryset, name, value):
        del name
        return queryset.search(value) if value else queryset


__all__ = ("FamilyMemberFilter",)

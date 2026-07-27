"""
Filters for the Family Members module.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.family_members.constants import (
    FamilyMemberGender,
    FamilyMemberRelationship,
    FamilyMemberStatus,
)
from apps.patient_management.family_members.models import (
    FamilyMember,
)

__all__ = [
    "FamilyMemberFilter",
]


class FamilyMemberFilter(
    django_filters.FilterSet,
):
    """
    FilterSet for FamilyMember.
    """

    search = django_filters.CharFilter(
        method="filter_search",
    )

    patient = django_filters.UUIDFilter(
        field_name="patient__id",
    )

    organization = django_filters.UUIDFilter(
        field_name="organization__id",
    )

    relationship = django_filters.ChoiceFilter(
        field_name="relationship",
        choices=FamilyMemberRelationship.choices,
    )

    gender = django_filters.ChoiceFilter(
        field_name="gender",
        choices=FamilyMemberGender.choices,
    )

    status = django_filters.ChoiceFilter(
        field_name="status",
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
            "organization",
            "relationship",
            "gender",
            "status",
            "is_living",
            "is_next_of_kin",
            "is_emergency_contact",
            "is_active",
        )

    def filter_search(
        self,
        queryset,
        name,
        value,
    ):
        """
        Apply free-text search.
        """
        del name

        if not value:
            return queryset

        return queryset.search(
            value,
        )

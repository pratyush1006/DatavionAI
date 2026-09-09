"""
API filters for Emergency Contacts.
"""

from __future__ import annotations

import django_filters

from ...constants import (
    EmergencyContactAvailability,
    EmergencyContactRelationship,
    EmergencyContactStatus,
    PreferredContactMethod,
)
from ...models import EmergencyContact


class EmergencyContactFilter(
    django_filters.FilterSet,
):
    """
    Filter EmergencyContact querysets.

    Authorization and organization scoping are handled by the selector,
    policy, and workflow layers.
    """

    search = django_filters.CharFilter(
        method="filter_search",
    )

    patient = django_filters.UUIDFilter(
        field_name="patient_id",
    )

    relationship = django_filters.ChoiceFilter(
        choices=EmergencyContactRelationship.choices,
    )

    status = django_filters.ChoiceFilter(
        choices=EmergencyContactStatus.choices,
    )

    preferred_contact_method = django_filters.ChoiceFilter(
        choices=PreferredContactMethod.choices,
    )

    availability = django_filters.ChoiceFilter(
        choices=EmergencyContactAvailability.choices,
    )

    is_primary = django_filters.BooleanFilter()

    is_verified = django_filters.BooleanFilter()

    is_legal_guardian = django_filters.BooleanFilter()

    has_medical_power_of_attorney = django_filters.BooleanFilter()

    priority_order = django_filters.NumberFilter()

    priority_order_min = django_filters.NumberFilter(
        field_name="priority_order",
        lookup_expr="gte",
    )

    priority_order_max = django_filters.NumberFilter(
        field_name="priority_order",
        lookup_expr="lte",
    )

    class Meta:
        model = EmergencyContact

        fields = (
            "patient",
            "relationship",
            "status",
            "preferred_contact_method",
            "availability",
            "is_primary",
            "is_verified",
            "is_legal_guardian",
            "has_medical_power_of_attorney",
            "priority_order",
        )

    def filter_search(
        self,
        queryset,
        name,
        value,
    ):
        return queryset.search(value)


__all__ = [
    "EmergencyContactFilter",
]

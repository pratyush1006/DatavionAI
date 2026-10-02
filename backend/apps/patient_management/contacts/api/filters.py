"""
Filters for the Patient Contacts API.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.contacts.models import Contact


class ContactFilter(
    django_filters.FilterSet,
):
    """
    Organization-scoped filters for patient contacts.

    Organization filtering is intentionally omitted from the client-facing
    filter contract because tenant and organization context are resolved
    server-side.
    """

    contact_type = django_filters.CharFilter(
        field_name="contact_type",
        lookup_expr="exact",
    )

    purpose = django_filters.CharFilter(
        field_name="purpose",
        lookup_expr="exact",
    )

    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="exact",
    )

    source = django_filters.CharFilter(
        field_name="source",
        lookup_expr="exact",
    )

    is_primary = django_filters.BooleanFilter(
        field_name="is_primary",
    )

    is_preferred = django_filters.BooleanFilter(
        field_name="is_preferred",
    )

    patient_id = django_filters.UUIDFilter(
        field_name="patient_id",
        lookup_expr="exact",
    )

    class Meta:
        model = Contact
        fields = (
            "contact_type",
            "purpose",
            "status",
            "source",
            "is_primary",
            "is_preferred",
            "patient_id",
        )


__all__ = ("ContactFilter",)

from __future__ import annotations

import django_filters

from apps.patient_management.relationships.models import PatientRelationship


class PatientRelationshipFilter(django_filters.FilterSet):
    relationship_type = django_filters.CharFilter(
        field_name="relationship_type", lookup_expr="iexact"
    )
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    verification_status = django_filters.CharFilter(
        field_name="verification_status", lookup_expr="iexact"
    )
    is_primary = django_filters.BooleanFilter(field_name="is_primary")
    is_active = django_filters.BooleanFilter(field_name="is_active")
    related_patient = django_filters.UUIDFilter(field_name="related_patient_id")

    class Meta:
        model = PatientRelationship
        fields = (
            "relationship_type",
            "status",
            "verification_status",
            "is_primary",
            "is_active",
            "related_patient",
        )

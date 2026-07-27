"""
Filters for the Patient Relationships API.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class RelationshipFilter(django_filters.FilterSet):
    """
    FilterSet for patient relationships.
    """

    class Meta:
        model = PatientRelationship
        fields = {
            "organization": ["exact"],
            "patient": ["exact"],
            "related_patient": ["exact"],
            "relationship_type": ["exact"],
            "status": ["exact"],
            "verification_status": ["exact"],
            "source": ["exact"],
            "is_primary": ["exact"],
        }


__all__ = [
    "RelationshipFilter",
]

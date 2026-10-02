"""
Filters for the Patient Identifiers API.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.identifiers.models import PatientIdentifier


class PatientIdentifierFilter(django_filters.FilterSet):
    """
    FilterSet for patient identifiers.
    """

    class Meta:
        model = PatientIdentifier
        fields = {
            "identifier_type": ["exact"],
            "status": ["exact"],
            "verification_status": ["exact"],
            "source": ["exact"],
            "is_primary": ["exact"],
            "patient": ["exact"],
            "organization": ["exact"],
        }


__all__ = [
    "PatientIdentifierFilter",
]

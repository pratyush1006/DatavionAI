"""
Filters for Patient Documents.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


class PatientDocumentFilter(
    django_filters.FilterSet,
):
    """
    Filter set for PatientDocument.
    """

    category = django_filters.CharFilter()

    status = django_filters.CharFilter()

    visibility = django_filters.CharFilter()

    storage_backend = django_filters.CharFilter()

    patient = django_filters.UUIDFilter(
        field_name="patient__id",
    )

    organization = django_filters.UUIDFilter(
        field_name="organization__id",
    )

    title = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    class Meta:
        model = PatientDocument

        fields = (
            "organization",
            "patient",
            "category",
            "status",
            "visibility",
            "storage_backend",
        )

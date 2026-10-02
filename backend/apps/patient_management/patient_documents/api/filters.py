"""Filters for Patient Documents API."""

from __future__ import annotations

import django_filters

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


class PatientDocumentFilter(
    django_filters.FilterSet,
):
    """Filter patient documents by patient, category, and status."""

    patient = django_filters.UUIDFilter(
        field_name="patient_id",
    )

    category = django_filters.CharFilter(
        field_name="category",
    )

    status = django_filters.CharFilter(
        field_name="status",
    )

    confidential = django_filters.BooleanFilter(
        field_name="is_confidential",
    )

    class Meta:
        """FilterSet metadata."""

        model = PatientDocument
        fields = (
            "patient",
            "category",
            "status",
            "confidential",
        )


__all__ = ("PatientDocumentFilter",)

"""Filters."""

from __future__ import annotations

from django_filters import rest_framework as filters

from apps.patient_management.medical_history.models import PatientMedicalHistory


class MedicalHistoryFilter(filters.FilterSet):
    """MedicalHistoryFilter implementation."""

    include_inactive = filters.BooleanFilter(method="filter_include_inactive")

    class Meta:
        """Meta implementation."""

        model = PatientMedicalHistory
        fields = (
            "patient",
            "organization",
            "history_type",
            "clinical_status",
            "is_active",
            "onset_date",
            "is_verified",
        )

    def filter_include_inactive(self, queryset, name, value):
        """Filter include inactive."""
        return queryset if value else queryset.filter(is_active=True)


__all__ = ("MedicalHistoryFilter",)

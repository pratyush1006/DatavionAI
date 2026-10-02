"""
Filtering helpers for Patient Referral API.
"""

from __future__ import annotations

from django_filters import rest_framework as filters

from apps.patient_management.referrals.models import PatientReferral


class PatientReferralFilter(filters.FilterSet):
    """Filter referrals by patient and lifecycle fields."""

    patient = filters.UUIDFilter(
        field_name="patient_id",
    )
    status = filters.CharFilter(
        field_name="status",
    )
    priority = filters.CharFilter(
        field_name="priority",
    )
    urgency = filters.CharFilter(
        field_name="urgency",
    )

    class Meta:
        """Filter metadata."""

        model = PatientReferral
        fields = (
            "patient",
            "status",
            "priority",
            "urgency",
        )


__all__ = ("PatientReferralFilter",)

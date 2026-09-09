"""
Filters for Patient Consent list endpoints.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.consents.models import (
    PatientConsent,
)


class PatientConsentFilter(
    django_filters.FilterSet,
):
    """
    Filter Patient Consent records by common domain fields.
    """

    class Meta:
        """
        Configure supported consent filters.
        """

        model = PatientConsent
        fields = (
            "patient",
            "organization",
            "purpose",
            "status",
        )


__all__ = ("PatientConsentFilter",)

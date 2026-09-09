"""
Appointment serializer field definitions.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.providers.models import Provider
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class AppointmentSerializerFields:
    """
    Shared serializer fields.
    """

    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
    )

    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
    )

    provider = serializers.PrimaryKeyRelatedField(
        queryset=Provider.objects.all(),
    )


__all__ = [
    "AppointmentSerializerFields",
]

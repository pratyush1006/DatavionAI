"""
API views for the Patient Identifiers module.
"""

from __future__ import annotations

from apps.common.api.base import (
    BaseCreateAPIView,
    BaseDestroyAPIView,
    BaseListAPIView,
    BaseRetrieveAPIView,
    BaseUpdateAPIView,
)
from apps.patient_management.identifiers.api.serializers.create import (
    PatientIdentifierCreateSerializer,
)
from apps.patient_management.identifiers.api.serializers.detail import (
    PatientIdentifierDetailSerializer,
)
from apps.patient_management.identifiers.api.serializers.list import (
    PatientIdentifierListSerializer,
)
from apps.patient_management.identifiers.api.serializers.update import (
    PatientIdentifierUpdateSerializer,
)
from apps.patient_management.identifiers.models import PatientIdentifier


class PatientIdentifierListAPIView(BaseListAPIView):
    """
    List patient identifiers.
    """

    queryset = PatientIdentifier.objects.all()
    serializer_class = PatientIdentifierListSerializer


class PatientIdentifierRetrieveAPIView(BaseRetrieveAPIView):
    """
    Retrieve a patient identifier.
    """

    queryset = PatientIdentifier.objects.all()
    serializer_class = PatientIdentifierDetailSerializer


class PatientIdentifierCreateAPIView(BaseCreateAPIView):
    """
    Create a patient identifier.
    """

    queryset = PatientIdentifier.objects.all()
    serializer_class = PatientIdentifierCreateSerializer


class PatientIdentifierUpdateAPIView(BaseUpdateAPIView):
    """
    Update a patient identifier.
    """

    queryset = PatientIdentifier.objects.all()
    serializer_class = PatientIdentifierUpdateSerializer


class PatientIdentifierDestroyAPIView(BaseDestroyAPIView):
    """
    Delete a patient identifier.
    """

    queryset = PatientIdentifier.objects.all()

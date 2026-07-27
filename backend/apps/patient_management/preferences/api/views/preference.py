"""
API views for PatientPreference.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseCreateAPIView,
    BaseDestroyAPIView,
    BaseListAPIView,
    BaseRetrieveAPIView,
    BaseUpdateAPIView,
)
from apps.patient_management.preferences.api.filters import (
    PatientPreferenceFilter,
)
from apps.patient_management.preferences.api.serializers import (
    PatientPreferenceCreateSerializer,
    PatientPreferenceDetailSerializer,
    PatientPreferenceListSerializer,
    PatientPreferenceUpdateSerializer,
)
from apps.patient_management.preferences.models import (
    PatientPreference,
)


class PatientPreferenceListAPIView(
    BaseListAPIView,
):
    """
    List patient preferences.
    """

    queryset = PatientPreference.objects.select_related(
        "organization",
        "patient",
    )

    serializer_class = PatientPreferenceListSerializer

    filterset_class = PatientPreferenceFilter


class PatientPreferenceDetailAPIView(
    BaseRetrieveAPIView,
):
    """
    Retrieve patient preferences.
    """

    queryset = PatientPreference.objects.select_related(
        "organization",
        "patient",
    )

    serializer_class = PatientPreferenceDetailSerializer

    lookup_field = "id"


class PatientPreferenceCreateAPIView(
    BaseCreateAPIView,
):
    """
    Create patient preferences.
    """

    serializer_class = PatientPreferenceCreateSerializer


class PatientPreferenceUpdateAPIView(
    BaseUpdateAPIView,
):
    """
    Update patient preferences.
    """

    queryset = PatientPreference.objects.all()

    serializer_class = PatientPreferenceUpdateSerializer

    lookup_field = "id"


class PatientPreferenceDeleteAPIView(
    BaseDestroyAPIView,
):
    """
    Delete patient preferences.
    """

    queryset = PatientPreference.objects.all()

    lookup_field = "id"

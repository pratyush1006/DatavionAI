"""
List API view for the Patient Registration module.
"""

from __future__ import annotations

from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)

from apps.common.api import BaseListAPIView
from apps.patient_management.registration.api.filters import (
    PatientRegistrationFilter,
)
from apps.patient_management.registration.api.serializers import (
    PatientRegistrationListSerializer,
)
from apps.patient_management.registration.models import (
    PatientRegistration,
)


class PatientRegistrationListAPIView(
    BaseListAPIView,
):
    """
    API view for listing registrations.
    """

    queryset = PatientRegistration.objects.all()

    serializer_class = PatientRegistrationListSerializer

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_class = PatientRegistrationFilter

    search_fields = (
        "registration_number",
        "patient__first_name",
        "patient__last_name",
        "patient__medical_record_number",
    )

    ordering_fields = (
        "registration_datetime",
        "registration_number",
        "created_at",
    )

    ordering = ("-registration_datetime",)

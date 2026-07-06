"""
API views for listing and creating appointments.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.appointments.api.serializers import (
    AppointmentCreateSerializer,
    AppointmentDetailSerializer,
    AppointmentListSerializer,
)
from apps.appointments.models import Appointment
from apps.appointments.permissions import (
    CanCreateAppointment,
    CanViewAppointment,
)
from apps.appointments.selectors import get_appointments
from apps.appointments.services import create_appointment
from apps.common.api.base_generics import BaseListCreateAPIView

APPOINTMENT_TAG: Final[tuple[str, ...]] = ("Appointments",)


@extend_schema(tags=APPOINTMENT_TAG)
class AppointmentListCreateAPIView(BaseListCreateAPIView):
    """
    List existing appointments or create a new appointment.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAppointment,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateAppointment,
        ),
    }

    serializer_classes = {
        "GET": AppointmentListSerializer,
        "POST": AppointmentCreateSerializer,
    }

    detail_serializer_class = AppointmentDetailSerializer

    create_service = create_appointment

    create_success_message = "Appointment created successfully."

    search_fields = (
        "appointment_number",
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
        "provider__provider_number",
    )

    ordering = ("-scheduled_start",)

    ordering_fields = (
        "appointment_number",
        "scheduled_start",
        "status",
        "priority",
        "created_at",
    )

    filterset_fields = (
        "appointment_type",
        "status",
        "priority",
        "is_virtual",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Appointment]:
        """
        Return the appointments queryset.
        """

        return get_appointments()


__all__ = [
    "AppointmentListCreateAPIView",
]

"""
API views for retrieving, updating, and deleting appointments.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.appointments.api.serializers import (
    AppointmentDetailSerializer,
    AppointmentUpdateSerializer,
)
from apps.appointments.models import Appointment
from apps.appointments.permissions import (
    CanDeleteAppointment,
    CanUpdateAppointment,
    CanViewAppointment,
)
from apps.appointments.selectors import get_appointment_by_id
from apps.appointments.services import (
    delete_appointment,
    update_appointment,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)

APPOINTMENT_TAG: Final[tuple[str, ...]] = (
    "Appointments",
)


@extend_schema(tags=APPOINTMENT_TAG)
class AppointmentRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an appointment.
    """

    lookup_url_kwarg = "appointment_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAppointment,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateAppointment,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateAppointment,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteAppointment,
        ),
    }

    serializer_classes = {
        "GET": AppointmentDetailSerializer,
        "PUT": AppointmentUpdateSerializer,
        "PATCH": AppointmentUpdateSerializer,
    }

    detail_serializer_class = (
        AppointmentDetailSerializer
    )

    update_service = update_appointment

    delete_service = delete_appointment

    def get_object(
        self,
    ) -> Appointment:
        """
        Return the requested appointment.
        """

        return get_appointment_by_id(
            appointment_id=self.kwargs[
                self.lookup_url_kwarg
            ],
        )


__all__ = [
    "AppointmentRetrieveUpdateDestroyAPIView",
]

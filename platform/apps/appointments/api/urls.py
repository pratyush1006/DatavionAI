"""
Appointment API URLs.
"""

from django.urls import path

from apps.appointments.api.views import (
    AppointmentListCreateAPIView,
    AppointmentRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        AppointmentListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:appointment_id>/",
        AppointmentRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "urlpatterns",
]

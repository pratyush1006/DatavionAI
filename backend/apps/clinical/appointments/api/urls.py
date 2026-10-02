"""Clinical Appointment API URL routes."""

from __future__ import annotations

from django.urls import path

from apps.clinical.appointments.api.views import (
    AppointmentCancelView,
    AppointmentCheckInView,
    AppointmentCompleteView,
    AppointmentConfirmView,
    AppointmentDepositCheckoutView,
    AppointmentDepositVerifyView,
    AppointmentDetailView,
    AppointmentListCreateView,
    AppointmentNoShowView,
    AppointmentRescheduleView,
    AppointmentStartView,
    AppointmentTrackView,
)

urlpatterns = [
    path(
        "track/<str:tracking_token>/",
        AppointmentTrackView.as_view(),
        name="appointment-track",
    ),
    path(
        "",
        AppointmentListCreateView.as_view(),
        name="appointment-list-create",
    ),
    path(
        "<uuid:appointment_id>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
    path(
        "<uuid:appointment_id>/confirm/",
        AppointmentConfirmView.as_view(),
        name="appointment-confirm",
    ),
    path(
        "<uuid:appointment_id>/deposit/checkout/",
        AppointmentDepositCheckoutView.as_view(),
        name="appointment-deposit-checkout",
    ),
    path(
        "<uuid:appointment_id>/deposit/verify/",
        AppointmentDepositVerifyView.as_view(),
        name="appointment-deposit-verify",
    ),
    path(
        "<uuid:appointment_id>/reschedule/",
        AppointmentRescheduleView.as_view(),
        name="appointment-reschedule",
    ),
    path(
        "<uuid:appointment_id>/cancel/",
        AppointmentCancelView.as_view(),
        name="appointment-cancel",
    ),
    path(
        "<uuid:appointment_id>/check-in/",
        AppointmentCheckInView.as_view(),
        name="appointment-check-in",
    ),
    path(
        "<uuid:appointment_id>/start/",
        AppointmentStartView.as_view(),
        name="appointment-start",
    ),
    path(
        "<uuid:appointment_id>/complete/",
        AppointmentCompleteView.as_view(),
        name="appointment-complete",
    ),
    path(
        "<uuid:appointment_id>/no-show/",
        AppointmentNoShowView.as_view(),
        name="appointment-no-show",
    ),
]


__all__ = ("urlpatterns",)

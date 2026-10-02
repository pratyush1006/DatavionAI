"""
Patient Portal API URL configuration.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.portal.api.views import (
    PatientPortalAccountDetailAPIView,
    PatientPortalAccountInvitationAPIView,
    PatientPortalAccountLifecycleAPIView,
    PatientPortalAccountListCreateAPIView,
    PatientPortalAccountRestoreAPIView,
)
from apps.patient_management.portal.api.views.dashboard import (
    PatientSelfDashboardAPIView,
)

urlpatterns = [
    path(
        "me/dashboard/",
        PatientSelfDashboardAPIView.as_view(),
        name="patient-portal-dashboard",
    ),
    path(
        "",
        PatientPortalAccountListCreateAPIView.as_view(),
        name="patient-portal-list-create",
    ),
    path(
        "<uuid:account_id>/",
        PatientPortalAccountDetailAPIView.as_view(),
        name="patient-portal-detail",
    ),
    path(
        "<uuid:account_id>/invite/",
        PatientPortalAccountInvitationAPIView.as_view(),
        name="patient-portal-invite",
    ),
    path(
        "<uuid:account_id>/lifecycle/",
        PatientPortalAccountLifecycleAPIView.as_view(),
        name="patient-portal-lifecycle",
    ),
    path(
        "<uuid:account_id>/restore/",
        PatientPortalAccountRestoreAPIView.as_view(),
        name="patient-portal-restore",
    ),
]

__all__ = ("urlpatterns",)

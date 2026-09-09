"""
Emergency Contacts API URLs.
"""

from django.urls import path

from apps.patient_management.emergency_contacts.api.views import (
    EmergencyContactActivateAPIView,
    EmergencyContactBlockAPIView,
    EmergencyContactDeactivateAPIView,
    EmergencyContactListCreateAPIView,
    EmergencyContactRetrieveUpdateDestroyAPIView,
    EmergencyContactSetPrimaryAPIView,
    EmergencyContactVerifyAPIView,
)

app_name = "patient-emergency-contacts"


urlpatterns = (
    path(
        "",
        EmergencyContactListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:emergency_contact_id>/",
        EmergencyContactRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path(
        "<uuid:emergency_contact_id>/verify/",
        EmergencyContactVerifyAPIView.as_view(),
        name="verify",
    ),
    path(
        "<uuid:emergency_contact_id>/activate/",
        EmergencyContactActivateAPIView.as_view(),
        name="activate",
    ),
    path(
        "<uuid:emergency_contact_id>/deactivate/",
        EmergencyContactDeactivateAPIView.as_view(),
        name="deactivate",
    ),
    path(
        "<uuid:emergency_contact_id>/block/",
        EmergencyContactBlockAPIView.as_view(),
        name="block",
    ),
    path(
        "<uuid:emergency_contact_id>/set-primary/",
        EmergencyContactSetPrimaryAPIView.as_view(),
        name="set-primary",
    ),
)


__all__ = (
    "app_name",
    "urlpatterns",
)

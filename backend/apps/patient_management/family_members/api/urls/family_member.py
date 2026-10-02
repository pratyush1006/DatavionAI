"""
URL patterns for the Patient Family Members API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.family_members.api.views import (
    FamilyMemberActivateAPIView,
    FamilyMemberDeactivateAPIView,
    FamilyMemberListCreateAPIView,
    FamilyMemberRestoreAPIView,
    FamilyMemberRetrieveUpdateDestroyAPIView,
    FamilyMemberSetEmergencyContactAPIView,
    FamilyMemberSetNextOfKinAPIView,
)

app_name = "patient-family-members"


urlpatterns = (
    path(
        "",
        FamilyMemberListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:family_member_id>/",
        FamilyMemberRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path(
        "<uuid:family_member_id>/activate/",
        FamilyMemberActivateAPIView.as_view(),
        name="activate",
    ),
    path(
        "<uuid:family_member_id>/deactivate/",
        FamilyMemberDeactivateAPIView.as_view(),
        name="deactivate",
    ),
    path(
        "<uuid:family_member_id>/restore/",
        FamilyMemberRestoreAPIView.as_view(),
        name="restore",
    ),
    path(
        "<uuid:family_member_id>/set-next-of-kin/",
        FamilyMemberSetNextOfKinAPIView.as_view(),
        name="set-next-of-kin",
    ),
    path(
        "<uuid:family_member_id>/set-emergency-contact/",
        FamilyMemberSetEmergencyContactAPIView.as_view(),
        name="set-emergency-contact",
    ),
)


__all__ = (
    "app_name",
    "urlpatterns",
)

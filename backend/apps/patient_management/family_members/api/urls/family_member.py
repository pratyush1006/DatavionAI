"""
URL patterns for the Family Members API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.family_members.api.views import (
    FamilyMemberCreateAPIView,
    FamilyMemberDeleteAPIView,
    FamilyMemberDetailAPIView,
    FamilyMemberListAPIView,
    FamilyMemberUpdateAPIView,
)

app_name = "family-members-api"

urlpatterns = [
    path(
        "",
        FamilyMemberListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        FamilyMemberCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:id>/",
        FamilyMemberDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:id>/update/",
        FamilyMemberUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:id>/delete/",
        FamilyMemberDeleteAPIView.as_view(),
        name="delete",
    ),
]

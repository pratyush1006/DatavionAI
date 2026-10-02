"""Organization access-control URLs."""

from __future__ import annotations

from django.urls import path

from apps.datavionos.access_control.api.views import (
    DepartmentMemberAssignmentAPIView,
    DepartmentMemberLifecycleAPIView,
    OrganizationAccessControlAPIView,
    OrganizationDepartmentCreateAPIView,
    OrganizationMemberOnboardingAPIView,
    OrganizationRoleAssignmentAPIView,
    OrganizationRoleLifecycleAPIView,
    OrganizationTeamCreateAPIView,
)

app_name = "organization-access-control"
urlpatterns = [
    path("", OrganizationAccessControlAPIView.as_view(), name="snapshot"),
    path(
        "departments/",
        OrganizationDepartmentCreateAPIView.as_view(),
        name="department-create",
    ),
    path("teams/", OrganizationTeamCreateAPIView.as_view(), name="team-create"),
    path(
        "members/onboard/",
        OrganizationMemberOnboardingAPIView.as_view(),
        name="member-onboard",
    ),
    path(
        "roles/assign/", OrganizationRoleAssignmentAPIView.as_view(), name="role-assign"
    ),
    path(
        "roles/<uuid:assignment_id>/lifecycle/",
        OrganizationRoleLifecycleAPIView.as_view(),
        name="role-lifecycle",
    ),
    path(
        "department-members/assign/",
        DepartmentMemberAssignmentAPIView.as_view(),
        name="department-member-assign",
    ),
    path(
        "department-members/<uuid:membership_id>/lifecycle/",
        DepartmentMemberLifecycleAPIView.as_view(),
        name="department-member-lifecycle",
    ),
]

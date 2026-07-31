"""
Employee API routes.

Includes:

- CRUD endpoints
- Employee lifecycle workflow endpoints
"""

from __future__ import annotations

from django.urls import path

from apps.organization.employees.api.views import (
    EmployeeActivateAPIView,
    EmployeeAssignmentAPIView,
    EmployeeContractAPIView,
    EmployeeDeactivateAPIView,
    EmployeeListCreateAPIView,
    EmployeeOffboardingAPIView,
    EmployeeOnboardingAPIView,
    EmployeeRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # ========================================================
    # CRUD
    # ========================================================
    path(
        "",
        EmployeeListCreateAPIView.as_view(),
        name="employee-list-create",
    ),
    path(
        "<uuid:employee_id>/",
        EmployeeRetrieveUpdateDestroyAPIView.as_view(),
        name="employee-detail",
    ),
    # ========================================================
    # Lifecycle
    # ========================================================
    path(
        "<uuid:employee_id>/activate/",
        EmployeeActivateAPIView.as_view(),
        name="employee-activate",
    ),
    path(
        "<uuid:employee_id>/deactivate/",
        EmployeeDeactivateAPIView.as_view(),
        name="employee-deactivate",
    ),
    path(
        "<uuid:employee_id>/assignment/",
        EmployeeAssignmentAPIView.as_view(),
        name="employee-assignment",
    ),
    path(
        "<uuid:employee_id>/contract/",
        EmployeeContractAPIView.as_view(),
        name="employee-contract",
    ),
    path(
        "<uuid:employee_id>/offboard/",
        EmployeeOffboardingAPIView.as_view(),
        name="employee-offboard",
    ),
    path(
        "onboard/",
        EmployeeOnboardingAPIView.as_view(),
        name="employee-onboard",
    ),
]


__all__ = ("urlpatterns",)

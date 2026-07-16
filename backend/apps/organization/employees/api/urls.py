from apps.organization.employees.api.views import (
    EmployeeListCreateAPIView,
    EmployeeRetrieveUpdateDestroyAPIView,
)
from django.urls import path

urlpatterns = [
    path(
        "",
        EmployeeListCreateAPIView.as_view(),
        name="employee-list-create",
    ),
    path(
        "<int:employee_id>/",
        EmployeeRetrieveUpdateDestroyAPIView.as_view(),
        name="employee-detail",
    ),
]

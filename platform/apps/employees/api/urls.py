from django.urls import path

from apps.employees.api.views import (
    EmployeeListCreateAPIView,
    EmployeeRetrieveUpdateDestroyAPIView,
)

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

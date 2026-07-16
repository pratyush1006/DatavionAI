from apps.organization.departments.api.views import (
    DepartmentListCreateAPIView,
    DepartmentRetrieveUpdateDestroyAPIView,
)
from django.urls import path

urlpatterns = [
    path(
        "",
        DepartmentListCreateAPIView.as_view(),
        name="department-list-create",
    ),
    path(
        "<int:department_id>/",
        DepartmentRetrieveUpdateDestroyAPIView.as_view(),
        name="department-detail",
    ),
]

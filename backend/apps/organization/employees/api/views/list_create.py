"""
API views for listing and creating employees.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.organization.employees.api.serializers import (
    EmployeeCreateSerializer,
    EmployeeDetailSerializer,
    EmployeeListSerializer,
)
from apps.organization.employees.models import Employee
from apps.organization.employees.permissions import (
    CanCreateEmployee,
    CanViewEmployee,
)
from apps.organization.employees.selectors import (
    get_employees,
)
from apps.organization.employees.services import (
    create_employee,
)
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

EMPLOYEE_TAG: Final[tuple[str, ...]] = ("Employees",)


@extend_schema(tags=EMPLOYEE_TAG)
class EmployeeListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing employees or create a new employee.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewEmployee,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateEmployee,
        ),
    }

    serializer_classes = {
        "GET": EmployeeListSerializer,
        "POST": EmployeeCreateSerializer,
    }

    detail_serializer_class = EmployeeDetailSerializer

    create_service = create_employee

    create_success_message = "Employee created successfully."

    search_fields = (
        "employee_code",
        "user__first_name",
        "user__last_name",
        "user__email",
        "designation",
    )

    ordering = ("employee_code",)

    ordering_fields = (
        "employee_code",
        "hire_date",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "department",
        "team",
        "designation",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Employee]:
        """
        Return employees.
        """

        return get_employees()


__all__ = [
    "EmployeeListCreateAPIView",
]

"""
API views for retrieving, updating and deleting employees.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.organization.employees.api.serializers import (
    EmployeeDetailSerializer,
    EmployeeUpdateSerializer,
)
from apps.organization.employees.permissions import (
    CanDeleteEmployee,
    CanUpdateEmployee,
    CanViewEmployee,
)
from apps.organization.employees.selectors import (
    get_employee_by_id,
)
from apps.organization.employees.services import (
    delete_employee,
    update_employee,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

EMPLOYEE_TAG: Final[tuple[str, ...]] = ("Employees",)


@extend_schema(tags=EMPLOYEE_TAG)
class EmployeeRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete an employee.
    """

    lookup_url_kwarg = "employee_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewEmployee,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateEmployee,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateEmployee,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteEmployee,
        ),
    }

    serializer_classes = {
        "GET": EmployeeDetailSerializer,
        "PUT": EmployeeUpdateSerializer,
        "PATCH": EmployeeUpdateSerializer,
    }

    detail_serializer_class = EmployeeDetailSerializer

    update_service = update_employee

    delete_service = delete_employee

    update_success_message = "Employee updated successfully."

    def get_object(self):
        """
        Return the requested employee.
        """

        return get_employee_by_id(
            employee_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "EmployeeRetrieveUpdateDestroyAPIView",
]

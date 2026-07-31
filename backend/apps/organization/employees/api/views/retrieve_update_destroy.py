"""
API views for retrieving, updating, and deleting employees.

Architecture:

GET
    Selector driven

PUT/PATCH
    Workflow driven

DELETE
    Workflow driven
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

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
from apps.organization.employees.workflows import (
    EmployeeDeletionRequest,
    EmployeeDeletionWorkflow,
    EmployeeUpdateRequest,
    EmployeeUpdateWorkflow,
)

EMPLOYEE_TAG: Final[tuple[str, ...]] = ("Employees",)


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete employee.

    GET:
        Selector driven.

    PUT/PATCH:
        Workflow driven.

    DELETE:
        Workflow driven.
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
        "GET": (EmployeeDetailSerializer),
        "PUT": (EmployeeUpdateSerializer),
        "PATCH": (EmployeeUpdateSerializer),
    }

    detail_serializer_class = EmployeeDetailSerializer

    update_workflow = EmployeeUpdateWorkflow

    delete_workflow = EmployeeDeletionWorkflow

    update_success_message = "Employee updated successfully."

    delete_success_message = "Employee deleted successfully."

    def get_object(
        self,
    ):
        """
        Return employee instance.
        """

        return get_employee_by_id(
            employee_id=(self.kwargs[self.lookup_url_kwarg]),
        )

    def build_update_workflow_request(
        self,
        instance,
        validated_data,
    ) -> EmployeeUpdateRequest:
        """
        Build employee update workflow request.
        """

        return EmployeeUpdateRequest(
            employee_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance,
    ) -> EmployeeDeletionRequest:
        """
        Build employee deletion workflow request.
        """

        return EmployeeDeletionRequest(
            employee_id=instance.id,
        )


__all__ = ("EmployeeRetrieveUpdateDestroyAPIView",)

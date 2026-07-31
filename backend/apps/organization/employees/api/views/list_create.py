"""
API views for listing and creating employees.

Architecture:

GET
    Selector driven

POST
    Workflow driven
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.organization.employees.api.serializers import (
    EmployeeCreateSerializer,
    EmployeeDetailSerializer,
    EmployeeListSerializer,
)
from apps.organization.employees.models import (
    Employee,
)
from apps.organization.employees.permissions import (
    CanCreateEmployee,
    CanViewEmployee,
)
from apps.organization.employees.selectors import (
    get_employees,
)
from apps.organization.employees.workflows import (
    EmployeeCreationRequest,
    EmployeeCreationWorkflow,
)

EMPLOYEE_TAG: Final[tuple[str, ...]] = ("Employees",)


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List employees or create employee.

    GET:
        Selector driven.

    POST:
        Workflow driven.
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

    create_workflow = EmployeeCreationWorkflow

    create_success_message = "Employee created successfully."

    search_fields = (
        "employee_code",
        "work_email",
        "designation",
    )

    ordering = ("employee_code",)

    ordering_fields = (
        "employee_code",
        "designation",
        "joining_date",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "status",
        "employment_type",
    )

    def build_workflow_request(
        self,
        validated_data,
    ) -> EmployeeCreationRequest:
        """
        Build employee creation workflow request.
        """

        user = validated_data.get(
            "user",
        )

        return EmployeeCreationRequest(
            organization_id=(validated_data["organization"].id),
            employee_code=(validated_data["employee_code"]),
            designation=(validated_data["designation"]),
            joining_date=(validated_data["joining_date"]),
            user_id=(user.id if user else None),
            work_email=(
                validated_data.get(
                    "work_email",
                )
            ),
            phone_number=(
                validated_data.get(
                    "phone_number",
                )
            ),
            employment_type=(
                validated_data.get(
                    "employment_type",
                )
            ),
        )

    def get_queryset(
        self,
    ) -> QuerySet[Employee]:
        """
        Return organization scoped employees.
        """

        organization_id = self.request.query_params.get(
            "organization",
        )

        if organization_id is None:
            organization = getattr(
                self.request,
                "organization",
                None,
            )

            if organization is not None:
                organization_id = organization.id

        if organization_id is None:
            user = self.request.user

            organization_role = user.organization_roles.select_related(
                "organization",
            ).first()

            if organization_role is not None:
                organization_id = organization_role.organization.id

        if organization_id is None:
            return Employee.objects.none()

        return get_employees(
            organization_id=organization_id,
        )


__all__ = ("EmployeeListCreateAPIView",)

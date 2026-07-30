"""
API views for listing and creating departments.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.organization.departments.api.serializers import (
    DepartmentCreateSerializer,
    DepartmentDetailSerializer,
    DepartmentListSerializer,
)
from apps.organization.departments.models import (
    Department,
)
from apps.organization.departments.permissions import (
    CanCreateDepartment,
    CanViewDepartment,
)
from apps.organization.departments.selectors import (
    get_departments,
)
from apps.organization.departments.workflows import (
    DepartmentCreationRequest,
    DepartmentCreationWorkflow,
)

DEPARTMENT_TAG: Final[tuple[str, ...]] = ("Departments",)


@extend_schema(
    tags=DEPARTMENT_TAG,
)
class DepartmentListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing departments or create a new department.

    GET:
        Selector driven.

    POST:
        Workflow driven.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewDepartment,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateDepartment,
        ),
    }

    serializer_classes = {
        "GET": DepartmentListSerializer,
        "POST": DepartmentCreateSerializer,
    }

    detail_serializer_class = DepartmentDetailSerializer

    create_workflow = DepartmentCreationWorkflow

    create_success_message = "Department created successfully."

    search_fields = (
        "name",
        "code",
    )

    ordering = ("name",)

    ordering_fields = (
        "name",
        "code",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "is_active",
        "department_type",
        "status",
    )

    def build_workflow_request(
        self,
        validated_data,
    ) -> DepartmentCreationRequest:
        """
        Build department creation workflow request.
        """

        organization = validated_data["organization"]

        return DepartmentCreationRequest(
            organization_id=organization.id,
            name=validated_data["name"],
            code=validated_data["code"],
            description=validated_data.get(
                "description",
            ),
            department_type=validated_data.get(
                "department_type",
            ),
            phone=validated_data.get(
                "phone",
            ),
            email=validated_data.get(
                "email",
            ),
            location=validated_data.get(
                "location",
            ),
        )

    def get_queryset(
        self,
    ) -> QuerySet[Department]:
        """
        Return organization scoped departments.

        Selector requires organization_id.
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
            return Department.objects.none()

        return get_departments(
            organization_id=organization_id,
        )


__all__ = [
    "DepartmentListCreateAPIView",
]

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
from apps.departments.api.serializers import (
    DepartmentCreateSerializer,
    DepartmentDetailSerializer,
    DepartmentListSerializer,
)
from apps.departments.models import Department
from apps.departments.permissions import (
    CanCreateDepartment,
    CanViewDepartment,
)
from apps.departments.selectors import (
    get_departments,
)
from apps.departments.services import (
    create_department,
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

    create_service = create_department

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
    )

    def get_queryset(
        self,
    ) -> QuerySet[Department]:
        """
        Return the departments queryset.
        """

        return get_departments()


__all__ = [
    "DepartmentListCreateAPIView",
]

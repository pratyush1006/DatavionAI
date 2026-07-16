"""
API views for retrieving, updating, and deleting departments.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.organization.departments.api.serializers import (
    DepartmentDetailSerializer,
    DepartmentUpdateSerializer,
)
from apps.organization.departments.permissions import (
    CanDeleteDepartment,
    CanUpdateDepartment,
    CanViewDepartment,
)
from apps.organization.departments.selectors import (
    get_department_by_id,
)
from apps.organization.departments.services import (
    delete_department,
    update_department,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

DEPARTMENT_TAG: Final[tuple[str, ...]] = ("Departments",)


@extend_schema(
    tags=DEPARTMENT_TAG,
)
class DepartmentRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a department.
    """

    lookup_url_kwarg = "department_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewDepartment,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateDepartment,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateDepartment,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteDepartment,
        ),
    }

    serializer_classes = {
        "GET": DepartmentDetailSerializer,
        "PUT": DepartmentUpdateSerializer,
        "PATCH": DepartmentUpdateSerializer,
    }

    detail_serializer_class = DepartmentDetailSerializer

    update_service = update_department

    delete_service = delete_department

    update_success_message = "Department updated successfully."

    def get_object(
        self,
    ):
        """
        Return the requested department.
        """

        return get_department_by_id(
            department_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "DepartmentRetrieveUpdateDestroyAPIView",
]

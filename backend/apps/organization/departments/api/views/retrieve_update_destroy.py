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
from apps.organization.departments.workflows import (
    DepartmentDeletionRequest,
    DepartmentDeletionWorkflow,
    DepartmentUpdateRequest,
    DepartmentUpdateWorkflow,
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

    GET:
        Selector driven.

    PUT/PATCH:
        Workflow driven.

    DELETE:
        Workflow driven.
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

    update_workflow = DepartmentUpdateWorkflow

    delete_workflow = DepartmentDeletionWorkflow

    update_success_message = "Department updated successfully."

    delete_success_message = "Department deleted successfully."

    def get_object(
        self,
    ):
        """
        Return requested department.
        """

        return get_department_by_id(
            department_id=self.kwargs[self.lookup_url_kwarg],
        )

    def build_update_workflow_request(
        self,
        instance,
        validated_data,
    ) -> DepartmentUpdateRequest:
        """
        Build department update workflow request.
        """

        return DepartmentUpdateRequest(
            department_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance,
    ) -> DepartmentDeletionRequest:
        """
        Build department deletion workflow request.
        """

        return DepartmentDeletionRequest(
            department_id=instance.id,
        )


__all__ = [
    "DepartmentRetrieveUpdateDestroyAPIView",
]

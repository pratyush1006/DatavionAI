"""
Workflow API views for laboratory tests.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.clinical.laboratories.api.serializers.workflow import (
    LaboratoryTestWorkflowResponseSerializer,
)
from apps.clinical.laboratories.permissions import (
    IsLaboratoryTestUser,
)
from apps.clinical.laboratories.selectors import (
    list_laboratory_tests,
)
from apps.clinical.laboratories.services import (
    cancel_laboratory_test,
    complete_laboratory_test,
    start_laboratory_test,
)


class BaseLaboratoryTestWorkflowAPIView(
    GenericAPIView,
):
    """
    Base workflow API view for laboratory tests.
    """

    permission_classes = (IsLaboratoryTestUser,)

    serializer_class = LaboratoryTestWorkflowResponseSerializer

    workflow_service = None

    def get_object(
        self,
        uuid,
    ):
        """
        Return the laboratory test.
        """

        return list_laboratory_tests().get(
            id=uuid,
        )

    def post(
        self,
        request: Request,
        uuid,
    ) -> Response:
        """
        Execute the workflow.
        """

        instance = self.get_object(
            uuid,
        )

        instance = self.workflow_service(
            instance=instance,
        )

        serializer = self.get_serializer(
            {
                "success": True,
                "data": {
                    "id": str(instance.id),
                    "status": instance.status,
                },
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Laboratories"],
    responses=LaboratoryTestWorkflowResponseSerializer,
)
class LaboratoryTestStartAPIView(
    BaseLaboratoryTestWorkflowAPIView,
):
    """
    Start a laboratory test.
    """

    workflow_service = start_laboratory_test


@extend_schema(
    tags=["Laboratories"],
    responses=LaboratoryTestWorkflowResponseSerializer,
)
class LaboratoryTestCompleteAPIView(
    BaseLaboratoryTestWorkflowAPIView,
):
    """
    Complete a laboratory test.
    """

    workflow_service = complete_laboratory_test


@extend_schema(
    tags=["Laboratories"],
    responses=LaboratoryTestWorkflowResponseSerializer,
)
class LaboratoryTestCancelAPIView(
    BaseLaboratoryTestWorkflowAPIView,
):
    """
    Cancel a laboratory test.
    """

    workflow_service = cancel_laboratory_test


__all__ = [
    "LaboratoryTestStartAPIView",
    "LaboratoryTestCompleteAPIView",
    "LaboratoryTestCancelAPIView",
]

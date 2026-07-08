"""
Workflow API views for laboratory tests.
"""

from __future__ import annotations

from apps.laboratories.permissions import (
    IsLaboratoryTestUser,
)
from apps.laboratories.selectors import (
    list_laboratory_tests,
)
from apps.laboratories.services import (
    cancel_laboratory_test,
    complete_laboratory_test,
    start_laboratory_test,
)
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseLaboratoryTestWorkflowAPIView(APIView):
    """
    Base workflow view for laboratory tests.
    """

    permission_classes = (IsLaboratoryTestUser,)

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

        return Response(
            {
                "success": True,
                "data": {
                    "id": str(instance.id),
                    "status": instance.status,
                },
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Laboratories"],
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

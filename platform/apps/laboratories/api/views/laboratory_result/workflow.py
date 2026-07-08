"""
Workflow API views for laboratory results.
"""

from __future__ import annotations

from apps.laboratories.permissions import (
    IsLaboratoryResultUser,
)
from apps.laboratories.selectors import (
    list_laboratory_results,
)
from apps.laboratories.services import (
    amend_laboratory_result,
    invalidate_laboratory_result,
    record_laboratory_result,
    verify_laboratory_result,
)
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseLaboratoryResultWorkflowAPIView(
    APIView,
):
    """
    Base workflow API view for laboratory results.
    """

    permission_classes = (IsLaboratoryResultUser,)

    workflow_service = None

    def get_object(
        self,
        uuid,
    ):
        """
        Return the laboratory result.
        """

        return list_laboratory_results().get(
            id=uuid,
        )


@extend_schema(
    tags=["Laboratories"],
)
class LaboratoryResultRecordAPIView(
    BaseLaboratoryResultWorkflowAPIView,
):
    """
    Record a laboratory result.
    """

    def post(
        self,
        request: Request,
        uuid,
    ) -> Response:
        """
        Record the laboratory result.
        """

        instance = self.get_object(
            uuid,
        )

        instance = record_laboratory_result(
            laboratory_result_id=instance.id,
        )

        return Response(
            {
                "success": True,
                "status": instance.status,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Laboratories"],
)
class LaboratoryResultVerifyAPIView(
    BaseLaboratoryResultWorkflowAPIView,
):
    """
    Verify a laboratory result.
    """

    def post(
        self,
        request: Request,
        uuid,
    ) -> Response:
        """
        Verify the laboratory result.
        """

        instance = self.get_object(
            uuid,
        )

        instance = verify_laboratory_result(
            laboratory_result_id=instance.id,
            verified_by_id=request.user.provider.id,
        )

        return Response(
            {
                "success": True,
                "status": instance.status,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Laboratories"],
)
class LaboratoryResultAmendAPIView(
    BaseLaboratoryResultWorkflowAPIView,
):
    """
    Amend a laboratory result.
    """

    def post(
        self,
        request: Request,
        uuid,
    ) -> Response:
        """
        Amend the laboratory result.
        """

        instance = self.get_object(
            uuid,
        )

        instance = amend_laboratory_result(
            laboratory_result_id=instance.id,
            validated_data=request.data,
        )

        return Response(
            {
                "success": True,
                "status": instance.status,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Laboratories"],
)
class LaboratoryResultInvalidateAPIView(
    BaseLaboratoryResultWorkflowAPIView,
):
    """
    Invalidate a laboratory result.
    """

    def post(
        self,
        request: Request,
        uuid,
    ) -> Response:
        """
        Invalidate the laboratory result.
        """

        instance = self.get_object(
            uuid,
        )

        instance = invalidate_laboratory_result(
            laboratory_result_id=instance.id,
        )

        return Response(
            {
                "success": True,
                "status": instance.status,
            },
            status=status.HTTP_200_OK,
        )


__all__ = [
    "LaboratoryResultRecordAPIView",
    "LaboratoryResultVerifyAPIView",
    "LaboratoryResultAmendAPIView",
    "LaboratoryResultInvalidateAPIView",
]

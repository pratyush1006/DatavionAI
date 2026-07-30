"""
Workflow API views for laboratory results.
"""

from __future__ import annotations

from apps.clinical.laboratories.permissions import (
    IsLaboratoryResultUser,
)
from apps.clinical.laboratories.selectors import (
    list_laboratory_results,
)
from apps.clinical.laboratories.services import (
    amend_laboratory_result,
    invalidate_laboratory_result,
    record_laboratory_result,
    verify_laboratory_result,
)
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


#
# Temporary workflow serializers.
# These can later be moved to
# apps/laboratories/api/serializers/workflow.py
#
class LaboratoryResultWorkflowResponseSerializer(
    serializers.Serializer,
):
    """
    Workflow response serializer.
    """

    success = serializers.BooleanField()

    status = serializers.CharField()


class LaboratoryResultAmendRequestSerializer(
    serializers.Serializer,
):
    """
    Amend request serializer.
    """

    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class BaseLaboratoryResultWorkflowAPIView(
    APIView,
):
    """
    Base workflow API view for laboratory results.
    """

    permission_classes = (IsLaboratoryResultUser,)

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
    responses=LaboratoryResultWorkflowResponseSerializer,
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
    responses=LaboratoryResultWorkflowResponseSerializer,
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
    request=LaboratoryResultAmendRequestSerializer,
    responses=LaboratoryResultWorkflowResponseSerializer,
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
    responses=LaboratoryResultWorkflowResponseSerializer,
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

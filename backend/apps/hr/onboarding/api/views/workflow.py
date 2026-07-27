"""
Workflow API views for lifecycle processes.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hr.onboarding.permissions import CanUpdateLifecycleProcess
from apps.hr.onboarding.selectors import get_lifecycle_process_by_id
from apps.hr.onboarding.services import (
    cancel_lifecycle_process,
    complete_lifecycle_process,
)

ONBOARDING_TAG: Final[tuple[str, ...]] = ("Onboarding",)


class BaseLifecycleProcessWorkflowAPIView(APIView):
    """
    Base workflow API view for lifecycle processes.
    """

    def get_object(self, lifecycle_process_id):
        """
        Return the lifecycle process.
        """

        return get_lifecycle_process_by_id(
            lifecycle_process_id=lifecycle_process_id,
        )


@extend_schema(tags=ONBOARDING_TAG)
class LifecycleProcessCompleteAPIView(
    BaseLifecycleProcessWorkflowAPIView,
):
    """
    Mark a lifecycle process as completed. All mandatory tasks
    must already be completed or skipped.
    """

    permission_classes = (IsAuthenticated, CanUpdateLifecycleProcess)

    def post(self, request: Request, lifecycle_process_id) -> Response:
        instance = self.get_object(lifecycle_process_id)

        instance = complete_lifecycle_process(instance=instance)

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=ONBOARDING_TAG)
class LifecycleProcessCancelAPIView(
    BaseLifecycleProcessWorkflowAPIView,
):
    """
    Cancel an in-progress lifecycle process.
    """

    permission_classes = (IsAuthenticated, CanUpdateLifecycleProcess)

    def post(self, request: Request, lifecycle_process_id) -> Response:
        instance = self.get_object(lifecycle_process_id)

        instance = cancel_lifecycle_process(instance=instance)

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


__all__ = [
    "LifecycleProcessCompleteAPIView",
    "LifecycleProcessCancelAPIView",
]

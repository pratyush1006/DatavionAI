"""
Workflow API views for performance reviews.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hr.performance.api.serializers import (
    PerformanceReviewAcknowledgeSerializer,
)
from apps.hr.performance.permissions import (
    CanUpdatePerformanceReview,
)
from apps.hr.performance.selectors import get_performance_review_by_id
from apps.hr.performance.services import (
    acknowledge_performance_review,
    complete_performance_review,
    submit_performance_review,
)

PERFORMANCE_TAG: Final[tuple[str, ...]] = ("Performance",)


class BasePerformanceReviewWorkflowAPIView(APIView):
    """
    Base workflow API view for performance reviews.
    """

    def get_object(self, performance_review_id):
        """
        Return the performance review.
        """

        return get_performance_review_by_id(
            performance_review_id=performance_review_id,
        )


@extend_schema(tags=PERFORMANCE_TAG)
class PerformanceReviewSubmitAPIView(
    BasePerformanceReviewWorkflowAPIView,
):
    """
    Submit a draft performance review.
    """

    permission_classes = (IsAuthenticated, CanUpdatePerformanceReview)

    def post(self, request: Request, performance_review_id) -> Response:
        instance = self.get_object(performance_review_id)

        instance = submit_performance_review(instance=instance)

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=PERFORMANCE_TAG,
    request=PerformanceReviewAcknowledgeSerializer,
)
class PerformanceReviewAcknowledgeAPIView(
    BasePerformanceReviewWorkflowAPIView,
):
    """
    Acknowledge a submitted performance review.
    """

    permission_classes = (IsAuthenticated, CanUpdatePerformanceReview)

    def post(self, request: Request, performance_review_id) -> Response:
        serializer = PerformanceReviewAcknowledgeSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        instance = self.get_object(performance_review_id)

        instance = acknowledge_performance_review(
            instance=instance,
            employee_comments=serializer.validated_data.get(
                "employee_comments",
                "",
            ),
        )

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=PERFORMANCE_TAG)
class PerformanceReviewCompleteAPIView(
    BasePerformanceReviewWorkflowAPIView,
):
    """
    Mark an acknowledged performance review as completed.
    """

    permission_classes = (IsAuthenticated, CanUpdatePerformanceReview)

    def post(self, request: Request, performance_review_id) -> Response:
        instance = self.get_object(performance_review_id)

        instance = complete_performance_review(instance=instance)

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


__all__ = [
    "PerformanceReviewSubmitAPIView",
    "PerformanceReviewAcknowledgeAPIView",
    "PerformanceReviewCompleteAPIView",
]

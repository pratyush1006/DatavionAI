"""
Bulk prediction operations API view.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.api.serializers import (
    PredictionCreateSerializer,
    PredictionDetailSerializer,
    RecommendationCreateSerializer,
    RecommendationDetailSerializer,
)
from apps.ai.services import (
    PredictionService,
    RecommendationService,
)
from apps.common.api.responses import success_response
from apps.common.permissions import IsAuthenticatedAndActive


class PredictionBulkCreateAPIView(APIView):
    """
    Bulk create predictions.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    serializer_class = PredictionCreateSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create multiple predictions.
        """

        serializer = self.serializer_class(
            data=request.data,
            many=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        predictions = PredictionService.bulk_create(
            validated_data_list=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = PredictionDetailSerializer(
            predictions,
            many=True,
        )

        return success_response(
            message="Predictions created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class RecommendationBulkCreateAPIView(APIView):
    """
    Bulk create recommendations.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    serializer_class = RecommendationCreateSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create multiple recommendations.
        """

        serializer = self.serializer_class(
            data=request.data,
            many=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        recommendations = RecommendationService.bulk_create(
            validated_data_list=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = RecommendationDetailSerializer(
            recommendations,
            many=True,
        )

        return success_response(
            message="Recommendations created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


__all__ = [
    "PredictionBulkCreateAPIView",
    "RecommendationBulkCreateAPIView",
]

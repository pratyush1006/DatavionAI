"""
API views for AI analyses.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.common.api.responses import success_response
from apps.imaging.api.serializers import (
    AIAnalysisCreateSerializer,
    AIAnalysisDetailSerializer,
    AIAnalysisListSerializer,
    AIAnalysisUpdateSerializer,
)
from apps.imaging.models import AIAnalysis
from apps.imaging.permissions import CanViewStudy
from apps.imaging.selectors import StudySelector
from apps.imaging.services import AIAnalysisService

AI_ANALYSIS_TAG: Final[tuple[str, ...]] = ("AI Analyses",)


@extend_schema(tags=AI_ANALYSIS_TAG)
class AIAnalysisListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating AI analyses.
    """

    permission_classes = (
        IsAuthenticated,
        CanViewStudy,
    )

    serializer_classes = {
        "GET": AIAnalysisListSerializer,
        "POST": AIAnalysisCreateSerializer,
    }

    detail_serializer_class = AIAnalysisDetailSerializer

    create_service = AIAnalysisService.create

    create_success_message = "AI analysis created successfully."

    search_fields = ("analysis_type",)

    ordering = ("-created_at",)

    ordering_fields = (
        "analysis_type",
        "confidence_score",
        "created_at",
    )

    filterset_fields = (
        "analysis_type",
        "is_reviewed",
    )

    def get_queryset(
        self,
    ) -> QuerySet[AIAnalysis]:
        """
        Return the AI analysis queryset.
        """

        return AIAnalysis.objects.select_related(
            "study",
            "ai_model",
        )


@extend_schema(tags=AI_ANALYSIS_TAG)
class AIAnalysisDetailAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an AI analysis.
    """

    lookup_url_kwarg = "analysis_id"

    permission_classes = (
        IsAuthenticated,
        CanViewStudy,
    )

    serializer_class = AIAnalysisDetailSerializer

    serializer_classes = {
        "GET": AIAnalysisDetailSerializer,
        "PUT": AIAnalysisUpdateSerializer,
        "PATCH": AIAnalysisUpdateSerializer,
    }

    update_service = AIAnalysisService.update

    def get_object(
        self,
    ) -> AIAnalysis:
        """
        Return the requested AI analysis.
        """

        return AIAnalysis.objects.get(
            pk=self.kwargs[self.lookup_url_kwarg],
        )


class StudyAIAnalysisAPIView(APIView):
    """
    List or create AI analyses for a specific study.
    """

    def get(
        self,
        request: Request,
        study_id: str,
    ) -> Response:
        """
        Return AI analyses for a study.
        """

        study = StudySelector.get(
            study_id=study_id,
        )

        analyses = study.ai_analyses.all()

        serializer = AIAnalysisListSerializer(
            analyses,
            many=True,
        )

        return success_response(
            data=serializer.data,
        )

    def post(
        self,
        request: Request,
        study_id: str,
    ) -> Response:
        """
        Create an AI analysis for a study.
        """

        study = StudySelector.get(
            study_id=study_id,
        )

        validated_data = {
            **request.data,
            "study": study.id,
        }

        serializer = AIAnalysisCreateSerializer(
            data=validated_data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        analysis = AIAnalysisService.create(
            validated_data=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = AIAnalysisDetailSerializer(analysis)

        return success_response(
            message="AI analysis created successfully.",
            data=response_serializer.data,
            status_code=201,
        )


__all__ = [
    "AIAnalysisDetailAPIView",
    "AIAnalysisListCreateAPIView",
    "StudyAIAnalysisAPIView",
]

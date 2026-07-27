"""
API views for imaging reports.
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
    ReportCreateSerializer,
    ReportDetailSerializer,
    ReportListSerializer,
    ReportUpdateSerializer,
)
from apps.imaging.models import Report
from apps.imaging.permissions import CanViewStudy
from apps.imaging.selectors import ReportSelector
from apps.imaging.services import ReportService

REPORT_TAG: Final[tuple[str, ...]] = ("Imaging Reports",)


@extend_schema(tags=REPORT_TAG)
class ReportListAPIView(BaseListCreateAPIView):
    """
    API view for listing imaging reports.
    """

    permission_classes = (
        IsAuthenticated,
        CanViewStudy,
    )

    serializer_classes = {
        "GET": ReportListSerializer,
        "POST": ReportCreateSerializer,
    }

    detail_serializer_class = ReportDetailSerializer

    create_service = ReportService.create

    create_success_message = "Report created successfully."

    search_fields = (
        "report_text",
        "findings",
        "impression",
    )

    ordering = ("-created_at",)

    ordering_fields = (
        "status",
        "created_at",
    )

    filterset_fields = ("status",)

    def get_queryset(
        self,
    ) -> QuerySet[Report]:
        """
        Return the report queryset.
        """

        return ReportSelector.queryset()


@extend_schema(tags=REPORT_TAG)
class ReportDetailAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an imaging report.
    """

    lookup_url_kwarg = "report_id"

    permission_classes = (
        IsAuthenticated,
        CanViewStudy,
    )

    serializer_class = ReportDetailSerializer

    serializer_classes = {
        "GET": ReportDetailSerializer,
        "PUT": ReportUpdateSerializer,
        "PATCH": ReportUpdateSerializer,
    }

    update_service = ReportService.update

    def get_object(
        self,
    ) -> Report:
        """
        Return the requested report.
        """

        return ReportSelector.get(
            report_id=self.kwargs[self.lookup_url_kwarg],
        )


class StudyReportAPIView(APIView):
    """
    Create or update a report for a specific study.
    """

    def get(
        self,
        request: Request,
        study_id: str,
    ) -> Response:
        """
        Return the report for a study.
        """

        report = ReportSelector.list_by_study(
            study_id=study_id,
        ).first()

        if not report:
            return Response(
                {"detail": "Report not found."},
                status=404,
            )

        serializer = ReportDetailSerializer(report)

        return success_response(
            data=serializer.data,
        )

    def post(
        self,
        request: Request,
        study_id: str,
    ) -> Response:
        """
        Create a report for a study.
        """

        validated_data = {
            **request.data,
            "study": study_id,
        }

        serializer = ReportCreateSerializer(
            data=validated_data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        report = ReportService.create(
            validated_data=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = ReportDetailSerializer(report)

        return success_response(
            message="Report created successfully.",
            data=response_serializer.data,
            status_code=201,
        )

    def put(
        self,
        request: Request,
        study_id: str,
    ) -> Response:
        """
        Update a report for a study.
        """

        report = ReportSelector.list_by_study(
            study_id=study_id,
        ).first()

        if not report:
            return Response(
                {"detail": "Report not found."},
                status=404,
            )

        serializer = ReportUpdateSerializer(
            report,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        updated_report = ReportService.update(
            instance=report,
            validated_data=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = ReportDetailSerializer(updated_report)

        return success_response(
            message="Report updated successfully.",
            data=response_serializer.data,
        )


__all__ = [
    "ReportDetailAPIView",
    "ReportListAPIView",
    "StudyReportAPIView",
]

"""
Report serializers for the Imaging application.
"""

from __future__ import annotations

from apps.imaging.api.serializers.fields import (
    REPORT_DETAIL_FIELDS,
    REPORT_LIST_FIELDS,
    REPORT_READ_ONLY_FIELDS,
    REPORT_UPDATE_FIELDS,
    REPORT_WRITE_FIELDS,
)
from apps.imaging.models import Report
from apps.imaging.services import ReportService


class ReportBaseSerializer:
    """
    Base serializer mixin for Report serializers.
    """

    class Meta:
        model = Report
        fields = ()


class ReportSerializer(
    ReportBaseSerializer,
):
    """
    Generic Report serializer.
    """

    class Meta(
        ReportBaseSerializer.Meta,
    ):
        fields = (
            "id",
            "study",
            "report_text",
            "findings",
            "impression",
            "recommendations",
            "reported_by",
            "status",
            "created_at",
            "updated_at",
        )


class ReportCreateSerializer(
    ReportBaseSerializer,
):
    """
    Serializer used for creating imaging reports.
    """

    class Meta(
        ReportBaseSerializer.Meta,
    ):
        fields = REPORT_WRITE_FIELDS
        read_only_fields = REPORT_READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create an imaging report.
        """

        return ReportService.create(
            validated_data=validated_data,
        )


class ReportUpdateSerializer(
    ReportBaseSerializer,
):
    """
    Serializer used for updating imaging reports.
    """

    class Meta(
        ReportBaseSerializer.Meta,
    ):
        fields = REPORT_UPDATE_FIELDS
        read_only_fields = REPORT_READ_ONLY_FIELDS

    def update(
        self,
        instance: Report,
        validated_data: dict[str, object],
    ) -> Report:
        """
        Update an imaging report.
        """

        return ReportService.update(
            instance=instance,
            validated_data=validated_data,
        )


class ReportListSerializer(
    ReportBaseSerializer,
):
    """
    Serializer used for listing imaging reports.
    """

    class Meta(
        ReportBaseSerializer.Meta,
    ):
        fields = REPORT_LIST_FIELDS
        read_only_fields = REPORT_READ_ONLY_FIELDS


class ReportDetailSerializer(
    ReportBaseSerializer,
):
    """
    Serializer used for retrieving imaging report details.
    """

    class Meta(
        ReportBaseSerializer.Meta,
    ):
        fields = REPORT_DETAIL_FIELDS
        read_only_fields = REPORT_READ_ONLY_FIELDS


__all__ = [
    "ReportCreateSerializer",
    "ReportDetailSerializer",
    "ReportListSerializer",
    "ReportSerializer",
    "ReportUpdateSerializer",
]

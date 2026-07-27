"""
API views for imaging studies.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
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
    StudyCreateSerializer,
    StudyDetailSerializer,
    StudyListSerializer,
    StudyUpdateSerializer,
)
from apps.imaging.models import Study
from apps.imaging.permissions import (
    CanCreateStudy,
    CanDeleteStudy,
    CanUpdateStudy,
    CanViewStudy,
)
from apps.imaging.selectors import StudySelector
from apps.imaging.services import StudyService

STUDY_TAG: Final[tuple[str, ...]] = ("Imaging Studies",)


@extend_schema(tags=STUDY_TAG)
class StudyListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing existing imaging studies and creating new ones.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewStudy,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateStudy,
        ),
    }

    serializer_classes = {
        "GET": StudyListSerializer,
        "POST": StudyCreateSerializer,
    }

    detail_serializer_class = StudyDetailSerializer

    create_service = StudyService.create

    create_success_message = "Imaging study created successfully."

    search_fields = (
        "study_instance_uid",
        "accession_number",
        "study_description",
        "referring_physician",
    )

    ordering = (
        "-study_date",
        "-created_at",
    )

    ordering_fields = (
        "study_date",
        "modality",
        "status",
        "created_at",
    )

    filterset_fields = (
        "modality",
        "status",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Study]:
        """
        Return the study queryset.
        """

        return StudySelector.queryset()


@extend_schema(tags=STUDY_TAG)
class StudyDetailAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an imaging study.
    """

    lookup_url_kwarg = "study_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewStudy,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateStudy,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateStudy,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteStudy,
        ),
    }

    serializer_class = StudyDetailSerializer

    serializer_classes = {
        "GET": StudyDetailSerializer,
        "PUT": StudyUpdateSerializer,
        "PATCH": StudyUpdateSerializer,
    }

    update_service = StudyService.update

    delete_service = StudyService.delete

    def get_object(
        self,
    ) -> Study:
        """
        Return the requested study.
        """

        return StudySelector.get(
            study_id=self.kwargs[self.lookup_url_kwarg],
        )


class StudyBulkCreateAPIView(APIView):
    """
    Bulk create imaging studies.
    """

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create multiple imaging studies.
        """

        serializer = StudyCreateSerializer(
            data=request.data,
            many=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        studies = StudyService.bulk_create(
            validated_data_list=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = StudyDetailSerializer(
            studies,
            many=True,
        )

        return success_response(
            message="Imaging studies created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


__all__ = [
    "StudyBulkCreateAPIView",
    "StudyDetailAPIView",
    "StudyListCreateAPIView",
]

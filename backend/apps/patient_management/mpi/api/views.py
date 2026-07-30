"""
API views for the Master Patient Index.
"""

from __future__ import annotations

from apps.common.api import BaseAPIView
from apps.common.api.pagination import StandardResultsSetPagination
from apps.common.api.responses import success_response
from apps.patient_management.mpi.api.filters import (
    MPIFilter,
)
from apps.patient_management.mpi.api.serializers import (
    MPICreateSerializer,
    MPIDetailSerializer,
    MPIListSerializer,
    MPIUpdateSerializer,
)
from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)
from apps.patient_management.mpi.permissions import (
    CanCreateMPI,
    CanDeleteMPI,
    CanUpdateMPI,
    CanViewMPI,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status


class MPIListAPIView(BaseAPIView):
    """
    List MPI records.
    """

    queryset = MasterPatientIndex.objects.select_related(
        "organization",
        "patient",
        "merged_into",
    ).all()

    serializer_class = MPIListSerializer
    permission_classes = (CanViewMPI,)
    pagination_class = StandardResultsSetPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filterset_class = MPIFilter

    search_fields = (
        "mpi_id",
        "abha_number",
        "aadhaar_number",
        "passport_number",
        "patient__first_name",
        "patient__last_name",
    )

    ordering_fields = (
        "mpi_id",
        "created_at",
    )

    ordering = ("-created_at",)


class MPIRetrieveAPIView(BaseAPIView):
    """
    Retrieve an MPI record.
    """

    queryset = MasterPatientIndex.objects.select_related(
        "organization",
        "patient",
        "merged_into",
    )

    serializer_class = MPIDetailSerializer
    permission_classes = (CanViewMPI,)


class MPICreateAPIView(BaseAPIView):
    """
    Create an MPI record.
    """

    queryset = MasterPatientIndex.objects.all()
    serializer_class = MPICreateSerializer
    permission_classes = (CanCreateMPI,)

    def perform_create(
        self,
        serializer: MPICreateSerializer,
    ) -> None:
        serializer.save()

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        response = super().create(
            request,
            *args,
            **kwargs,
        )

        return success_response(
            data=response.data,
            status_code=status.HTTP_201_CREATED,
        )


class MPIUpdateAPIView(BaseAPIView):
    """
    Update an MPI record.
    """

    queryset = MasterPatientIndex.objects.all()
    serializer_class = MPIUpdateSerializer
    permission_classes = (CanUpdateMPI,)


class MPIDestroyAPIView(BaseAPIView):
    """
    Delete an MPI record.
    """

    queryset = MasterPatientIndex.objects.all()
    serializer_class = MPIDetailSerializer
    permission_classes = (CanDeleteMPI,)

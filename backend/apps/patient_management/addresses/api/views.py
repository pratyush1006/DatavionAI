"""
API views for patient addresses.
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status

from apps.common.api import BaseAPIView
from apps.common.api.pagination import StandardResultsSetPagination
from apps.common.api.responses import success_response
from apps.patient_management.addresses.api.filters import (
    AddressFilter,
)
from apps.patient_management.addresses.api.serializers import (
    AddressCreateSerializer,
    AddressDetailSerializer,
    AddressListSerializer,
    AddressUpdateSerializer,
)
from apps.patient_management.addresses.models import Address
from apps.patient_management.addresses.permissions import (
    CanCreateAddress,
    CanDeleteAddress,
    CanUpdateAddress,
    CanViewAddress,
)


class AddressListAPIView(BaseAPIView):
    """
    List addresses.
    """

    queryset = Address.objects.select_related(
        "organization",
        "patient",
    ).all()
    serializer_class = AddressListSerializer
    permission_classes = (CanViewAddress,)
    pagination_class = StandardResultsSetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = AddressFilter
    search_fields = (
        "line_1",
        "city",
        "state",
        "country",
        "postal_code",
    )
    ordering_fields = (
        "city",
        "state",
        "country",
        "created_at",
    )
    ordering = ("-created_at",)


class AddressRetrieveAPIView(BaseAPIView):
    """
    Retrieve an address.
    """

    queryset = Address.objects.select_related(
        "organization",
        "patient",
    )
    serializer_class = AddressDetailSerializer
    permission_classes = (CanViewAddress,)


class AddressCreateAPIView(BaseAPIView):
    """
    Create an address.
    """

    queryset = Address.objects.all()
    serializer_class = AddressCreateSerializer
    permission_classes = (CanCreateAddress,)

    def perform_create(
        self,
        serializer: AddressCreateSerializer,
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


class AddressUpdateAPIView(BaseAPIView):
    """
    Update an address.
    """

    queryset = Address.objects.all()
    serializer_class = AddressUpdateSerializer
    permission_classes = (CanUpdateAddress,)


class AddressDestroyAPIView(BaseAPIView):
    """
    Delete an address.
    """

    queryset = Address.objects.all()
    serializer_class = AddressDetailSerializer
    permission_classes = (CanDeleteAddress,)

"""
List/create API for Patient Addresses.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.patient_management.addresses.api.filters import (
    AddressFilter,
)
from apps.patient_management.addresses.api.serializers import (
    AddressCreateSerializer,
    AddressDetailSerializer,
    AddressListSerializer,
)
from apps.patient_management.addresses.models import Address
from apps.patient_management.addresses.permissions import (
    CanCreateAddress,
    CanViewAddress,
)
from apps.patient_management.addresses.selectors import (
    AddressSelector,
)
from apps.patient_management.addresses.workflows import (
    AddressCreationRequest,
    AddressCreationWorkflow,
)

ADDRESS_TAG = ("Patient Addresses",)


@extend_schema(
    tags=ADDRESS_TAG,
)
class AddressListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    GET  -> selector driven.
    POST -> workflow driven.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAddress,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateAddress,
        ),
    }

    serializer_classes = {
        "GET": AddressListSerializer,
        "POST": AddressCreateSerializer,
    }

    detail_serializer_class = AddressDetailSerializer

    create_workflow = AddressCreationWorkflow

    create_success_message = "Patient address created successfully."

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filterset_class = AddressFilter

    search_fields = (
        "line_1",
        "line_2",
        "city",
        "state",
        "country",
        "postal_code",
        "patient__first_name",
        "patient__last_name",
        "patient__mrn",
    )

    ordering_fields = (
        "address_type",
        "address_use",
        "city",
        "state",
        "country",
        "status",
        "created_at",
    )

    ordering = (
        "-is_primary",
        "address_type",
        "-created_at",
    )

    def _get_organization(self):
        organization = getattr(
            self,
            "current_organization",
            None,
        )

        if organization is None:
            organization = getattr(
                self.request,
                "organization",
                None,
            )

        if organization is None:
            role = (
                self.request.user.organization_roles.select_related("organization")
                .filter(
                    is_active=True,
                )
                .first()
            )

            if role is not None:
                organization = role.organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        return organization

    def get_queryset(
        self,
    ) -> QuerySet[Address]:
        return AddressSelector.queryset(
            organization=self._get_organization(),
        )

    def build_workflow_request(
        self,
        validated_data: Mapping[str, Any],
    ) -> AddressCreationRequest:
        organization = self._get_organization()

        return AddressCreationRequest(
            organization_id=organization.id,
            patient_id=validated_data["patient"].id,
            data={
                key: value for key, value in validated_data.items() if key != "patient"
            },
        )

    def resolve_workflow_created_instance(
        self,
        result,
    ) -> Address:
        data = result.data

        if data is None:
            raise RuntimeError(
                "Address creation workflow returned no data.",
            )

        address_id = getattr(
            data,
            "address_id",
            None,
        )

        if address_id is None:
            raise RuntimeError(
                "Address creation workflow returned no address ID.",
            )

        return self.get_queryset().get(
            id=address_id,
        )


__all__ = ("AddressListCreateAPIView",)

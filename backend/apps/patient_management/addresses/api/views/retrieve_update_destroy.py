"""
Retrieve/update/delete API for Patient Addresses.
"""

from __future__ import annotations

from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.addresses.api.serializers import (
    AddressDetailSerializer,
    AddressUpdateSerializer,
)
from apps.patient_management.addresses.models import Address
from apps.patient_management.addresses.permissions import (
    CanDeleteAddress,
    CanUpdateAddress,
    CanViewAddress,
)
from apps.patient_management.addresses.selectors import (
    AddressSelector,
)
from apps.patient_management.addresses.workflows import (
    AddressDeletionRequest,
    AddressDeletionWorkflow,
    AddressUpdateRequest,
    AddressUpdateWorkflow,
)

ADDRESS_TAG = ("Patient Addresses",)


@extend_schema(
    tags=ADDRESS_TAG,
)
class AddressRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "address_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAddress,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateAddress,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateAddress,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteAddress,
        ),
    }

    serializer_classes = {
        "GET": AddressDetailSerializer,
        "PUT": AddressUpdateSerializer,
        "PATCH": AddressUpdateSerializer,
    }

    detail_serializer_class = AddressDetailSerializer

    update_workflow = AddressUpdateWorkflow
    delete_workflow = AddressDeletionWorkflow

    update_success_message = "Patient address updated successfully."

    delete_success_message = "Patient address deleted successfully."

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

    def get_object(
        self,
    ) -> Address:
        return AddressSelector.get(
            address_id=self.kwargs[self.lookup_url_kwarg],
            organization=self._get_organization(),
        )

    def build_update_workflow_request(
        self,
        instance: Address,
        validated_data: dict[str, Any],
    ) -> AddressUpdateRequest:
        return AddressUpdateRequest(
            address_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance: Address,
    ) -> AddressDeletionRequest:
        return AddressDeletionRequest(
            address_id=instance.id,
        )


__all__ = ("AddressRetrieveUpdateDestroyAPIView",)

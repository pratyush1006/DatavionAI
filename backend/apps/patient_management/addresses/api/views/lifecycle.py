"""
Patient Address lifecycle API endpoints.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import (
    error_response,
    success_response,
)
from apps.core.workflows import (
    WorkflowContext,
)
from apps.patient_management.addresses.api.serializers import (
    AddressDetailSerializer,
)
from apps.patient_management.addresses.permissions import (
    CanActivateAddress,
    CanDeactivateAddress,
    CanSetPrimaryAddress,
    CanVerifyAddress,
)
from apps.patient_management.addresses.selectors import (
    AddressSelector,
)
from apps.patient_management.addresses.workflows import (
    AddressActivationRequest,
    AddressActivationWorkflow,
    AddressDeactivationRequest,
    AddressDeactivationWorkflow,
    AddressPrimaryRequest,
    AddressPrimaryWorkflow,
    AddressVerificationRequest,
    AddressVerificationWorkflow,
)


def _resolve_organization(request):
    organization = getattr(
        request,
        "organization",
        None,
    )

    if organization is None:
        role = (
            request.user.organization_roles.select_related("organization")
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


def _resolve_tenant(
    request,
    organization,
):
    tenant = getattr(
        request,
        "tenant",
        None,
    )

    if tenant is not None:
        return tenant

    return organization.tenant


class AddressLifecycleAPIView(
    APIView,
):
    """
    Common lifecycle execution infrastructure.
    """

    permission_classes = (IsAuthenticated,)

    workflow_class = None

    def get_context(
        self,
    ) -> WorkflowContext:
        organization = _resolve_organization(
            self.request,
        )
        tenant = _resolve_tenant(
            self.request,
            organization,
        )

        return WorkflowContext(
            tenant_id=tenant.id,
            actor_id=self.request.user.id,
            request_id=getattr(
                self.request,
                "request_id",
                None,
            ),
        )

    def get_address(
        self,
    ):
        organization = _resolve_organization(
            self.request,
        )

        return AddressSelector.get(
            address_id=self.kwargs["address_id"],
            organization=organization,
        )

    def execute_workflow(
        self,
        *,
        request_data,
        workflow_class,
        request_serializer,
    ) -> Response:
        address = self.get_address()

        workflow = workflow_class(
            request=request_serializer(
                address.id,
                **request_data,
            ),
        )

        result = workflow.execute(
            context=self.get_context(),
        )

        if not result.success:
            return error_response(
                request=self.request,
                message=result.message,
            )

        organization = _resolve_organization(
            self.request,
        )

        refreshed = AddressSelector.get(
            address_id=address.id,
            organization=organization,
        )

        serializer = AddressDetailSerializer(
            refreshed,
            context={
                "request": self.request,
            },
        )

        return success_response(
            request=self.request,
            data=serializer.data,
            message=result.message,
            status_code=status.HTTP_200_OK,
        )


class AddressVerifyAPIView(
    AddressLifecycleAPIView,
):
    permission_classes = (
        IsAuthenticated,
        CanVerifyAddress,
    )

    def post(
        self,
        request,
        address_id,
    ):
        return self.execute_workflow(
            request_data={},
            workflow_class=AddressVerificationWorkflow,
            request_serializer=lambda address_pk, **kwargs: AddressVerificationRequest(
                address_id=address_pk,
            ),
        )


class AddressActivateAPIView(
    AddressLifecycleAPIView,
):
    permission_classes = (
        IsAuthenticated,
        CanActivateAddress,
    )

    def post(
        self,
        request,
        address_id,
    ):
        return self.execute_workflow(
            request_data={},
            workflow_class=AddressActivationWorkflow,
            request_serializer=lambda address_pk, **kwargs: AddressActivationRequest(
                address_id=address_pk,
            ),
        )


class AddressDeactivateAPIView(
    AddressLifecycleAPIView,
):
    permission_classes = (
        IsAuthenticated,
        CanDeactivateAddress,
    )

    def post(
        self,
        request,
        address_id,
    ):
        return self.execute_workflow(
            request_data={},
            workflow_class=AddressDeactivationWorkflow,
            request_serializer=lambda address_pk, **kwargs: AddressDeactivationRequest(
                address_id=address_pk,
            ),
        )


class AddressSetPrimaryAPIView(
    AddressLifecycleAPIView,
):
    permission_classes = (
        IsAuthenticated,
        CanSetPrimaryAddress,
    )

    def post(
        self,
        request,
        address_id,
    ):
        return self.execute_workflow(
            request_data={},
            workflow_class=AddressPrimaryWorkflow,
            request_serializer=lambda address_pk, **kwargs: AddressPrimaryRequest(
                address_id=address_pk,
            ),
        )


__all__ = (
    "AddressActivateAPIView",
    "AddressDeactivateAPIView",
    "AddressSetPrimaryAPIView",
    "AddressVerifyAPIView",
)

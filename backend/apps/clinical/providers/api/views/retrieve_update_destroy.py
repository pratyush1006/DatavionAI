"""
API views for retrieving, updating, and deactivating providers.

Architecture:

GET
    Selector driven

PUT/PATCH
    Workflow driven

DELETE
    Workflow driven
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.providers.api.serializers import (
    ProviderDetailSerializer,
    ProviderUpdateSerializer,
)
from apps.clinical.providers.permissions import (
    CanDeactivateProvider,
    CanUpdateProvider,
    CanViewProvider,
)
from apps.clinical.providers.selectors import (
    ProviderSelector,
)
from apps.clinical.providers.workflows import (
    ProviderDeactivationRequest,
    ProviderDeactivationWorkflow,
    ProviderUpdateRequest,
    ProviderUpdateWorkflow,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.core.workflows import (
    WorkflowContext,
)

PROVIDER_TAG: Final[tuple[str, ...]] = ("Providers",)


@extend_schema(
    tags=PROVIDER_TAG,
)
class ProviderRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or deactivate a provider.

    GET:
        Selector driven.

    PUT/PATCH:
        Workflow driven.

    DELETE:
        Workflow driven.
    """

    lookup_url_kwarg = "provider_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewProvider,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateProvider,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateProvider,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeactivateProvider,
        ),
    }

    serializer_classes = {
        "GET": ProviderDetailSerializer,
        "PUT": ProviderUpdateSerializer,
        "PATCH": ProviderUpdateSerializer,
    }

    detail_serializer_class = ProviderDetailSerializer

    update_workflow = ProviderUpdateWorkflow

    delete_workflow = ProviderDeactivationWorkflow

    update_success_message = "Provider updated successfully."

    delete_success_message = "Provider deactivated successfully."

    def build_update_workflow_request(
        self,
        instance,
        validated_data,
    ) -> ProviderUpdateRequest:
        """
        Build provider update workflow request.
        """

        return ProviderUpdateRequest(
            provider_id=self.kwargs[self.lookup_url_kwarg],
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance,
    ) -> ProviderDeactivationRequest:
        """
        Build provider deactivation workflow request.
        """

        return ProviderDeactivationRequest(
            provider_id=instance.id,
        )

    def get_object(
        self,
    ):
        """
        Return provider instance.
        """

        return ProviderSelector.get(
            provider_id=self.kwargs[self.lookup_url_kwarg],
        )

    def get_workflow_context(self) -> WorkflowContext:
        """Build tenant-aware workflow context for Provider updates."""
        tenant = self.current_tenant

        if tenant is None:
            organization = self.current_organization

            if organization is None:
                try:
                    instance = self.get_object()
                except Exception:
                    instance = None
                organization = getattr(instance, "organization", None)

            if organization is None:
                role = (
                    self.request.user.organization_roles.select_related(
                        "organization__tenant"
                    )
                    .filter(is_active=True)
                    .first()
                )
                organization = role.organization if role is not None else None

            if organization is not None:
                tenant = organization.tenant

        if tenant is None:
            raise RuntimeError("Tenant context is required.")

        return WorkflowContext(
            actor_id=self.request.user.id,
            tenant_id=tenant.id,
        )


__all__ = ("ProviderRetrieveUpdateDestroyAPIView",)

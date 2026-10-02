"""
API views for listing and creating providers.

Architecture:

GET
    Selector driven

POST
    Workflow driven
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.clinical.providers.api.serializers import (
    ProviderCreateSerializer,
    ProviderDetailSerializer,
    ProviderListSerializer,
)
from apps.clinical.providers.models import (
    Provider,
)
from apps.clinical.providers.permissions import (
    CanCreateProvider,
    CanViewProvider,
)
from apps.clinical.providers.selectors import (
    ProviderSelector,
)
from apps.clinical.providers.workflows import (
    ProviderCreationRequest,
    ProviderCreationWorkflow,
)
from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.core.workflows import (
    WorkflowContext,
)
from apps.platform.organizations.models import (
    Organization,
)

PROVIDER_TAG: Final[tuple[str, ...]] = ("Providers",)


@extend_schema(
    tags=PROVIDER_TAG,
)
class ProviderListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List providers or create provider.

    GET:
        Selector driven.

    POST:
        Workflow driven.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewProvider,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateProvider,
        ),
    }

    serializer_classes = {
        "GET": ProviderListSerializer,
        "POST": ProviderCreateSerializer,
    }

    detail_serializer_class = ProviderDetailSerializer

    create_workflow = ProviderCreationWorkflow

    create_success_message = "Provider created successfully."

    search_fields = (
        "provider_number",
        "employee__user__first_name",
        "employee__user__last_name",
    )

    ordering = ("provider_number",)

    ordering_fields = (
        "provider_number",
        "provider_type",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "provider_type",
        "status",
        "is_accepting_patients",
    )

    def resolve_workflow_created_instance(self, result):
        "Resolve ProviderCreationData.provider_id to the canonical Provider model."
        data = result.data
        if data is None:
            return None

        provider_id = getattr(data, "provider_id", None)
        if provider_id is not None:
            return self.get_queryset().get(id=provider_id)

        return super().resolve_workflow_created_instance(result)

    def get_workflow_context(self) -> WorkflowContext:
        "Build tenant-aware workflow context for Provider creation."
        tenant = self.current_tenant

        if tenant is None:
            organization = self.current_organization

            if organization is None:
                organization_id = getattr(
                    self,
                    "_workflow_organization_id",
                    None,
                )
                if organization_id is not None:
                    organization = Organization.objects.select_related(
                        "tenant",
                    ).get(
                        pk=organization_id,
                    )

            if organization is None:
                role = (
                    self.request.user.organization_roles.select_related(
                        "organization__tenant",
                    )
                    .filter(
                        is_active=True,
                    )
                    .first()
                )
                organization = role.organization if role is not None else None

            if organization is not None:
                tenant = organization.tenant

        if tenant is None:
            raise RuntimeError(
                "Tenant context is required.",
            )

        return WorkflowContext(
            actor_id=self.request.user.id,
            tenant_id=tenant.id,
        )

    def build_workflow_request(
        self,
        validated_data,
    ) -> ProviderCreationRequest:
        """
        Build provider creation workflow request.

        Organization resolution priority:

        1. request.organization
           (future tenant middleware)

        2. request.user.organization
           (current compatibility layer)

        3. serializer organization
        """

        employee = validated_data["employee"]

        organization = getattr(
            self.request,
            "organization",
            None,
        )

        if organization is None:
            organization = getattr(
                self.request.user,
                "organization",
                None,
            )

        if organization is None:
            organization = validated_data.get(
                "organization",
            )

        if organization is None:
            raise ValidationError(
                {"organization": ("Organization context is required.")}
            )

        self._workflow_organization_id = organization.id

        return ProviderCreationRequest(
            organization_id=organization.id,
            employee_id=employee.id,
            provider_number=(validated_data["provider_number"]),
            provider_type=(validated_data["provider_type"]),
            years_of_experience=(
                validated_data.get(
                    "years_of_experience",
                    0,
                )
            ),
            consultation_fee=validated_data.get(
                "consultation_fee",
                0,
            ),
            is_accepting_patients=(
                validated_data.get(
                    "is_accepting_patients",
                    True,
                )
            ),
            bio=(
                validated_data.get(
                    "bio",
                    "",
                )
            ),
        )

    def get_queryset(
        self,
    ) -> QuerySet[Provider]:
        """
        Return organization scoped providers.
        """

        organization_id = self.request.query_params.get(
            "organization",
        )

        organization = getattr(
            self.request,
            "organization",
            None,
        )

        if organization_id is None and organization is None:
            organization = getattr(
                self.request.user,
                "organization",
                None,
            )

        if organization_id is None and organization:
            organization_id = organization.id

        if organization_id is None:
            user = self.request.user

            organization_role = user.organization_roles.select_related(
                "organization",
            ).first()

            if organization_role:
                organization_id = organization_role.organization.id

        if organization_id is None:
            return Provider.objects.none()

        organization = self._get_organization(
            organization_id,
        )

        return ProviderSelector.list_by_organization(
            organization=organization,
        )

    def _get_organization(
        self,
        organization_id,
    ):
        """
        Resolve organization.
        """

        from apps.platform.organizations.models import (
            Organization,
        )

        return Organization.objects.get(
            id=organization_id,
        )


__all__ = ("ProviderListCreateAPIView",)

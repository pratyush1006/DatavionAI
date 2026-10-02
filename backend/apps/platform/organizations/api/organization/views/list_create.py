"""
API views for listing and creating organizations.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.platform.organizations.api.organization.serializers import (
    OrganizationCreateSerializer,
    OrganizationDetailSerializer,
    OrganizationListSerializer,
)
from apps.platform.organizations.models import Organization
from apps.platform.organizations.permissions.organization import (
    CanCreateOrganization,
    CanViewOrganization,
)
from apps.platform.organizations.selectors import get_organizations
from apps.platform.organizations.workflows import (
    OrganizationCreationRequest,
    OrganizationCreationWorkflow,
)
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

ORGANIZATION_TAG: Final[tuple[str, ...]] = ("Organizations",)


@extend_schema(
    tags=ORGANIZATION_TAG,
)
class OrganizationListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    API endpoint for listing and creating organizations.

    GET
        Returns organizations visible to the current user.

    POST
        Creates a new organization through the organization
        creation workflow.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganization,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateOrganization,
        ),
    }

    serializer_classes = {
        "GET": OrganizationListSerializer,
        "POST": OrganizationCreateSerializer,
    }

    detail_serializer_class = OrganizationDetailSerializer

    create_workflow = OrganizationCreationWorkflow

    create_success_message = "Organization created successfully."

    search_fields = (
        "name",
        "display_name",
        "code",
        "city",
        "state",
        "country",
    )

    ordering = ("name",)

    ordering_fields = (
        "name",
        "display_name",
        "code",
        "city",
        "created_at",
        "updated_at",
    )

    filterset_fields = (
        "category",
        "organization_type",
        "status",
        "verification_status",
        "country",
    )

    def build_workflow_request(
        self,
        validated_data,
    ) -> OrganizationCreationRequest:
        """
        Build the organization creation workflow request.

        The API serializer remains responsible for validation and
        normalization. The workflow request carries the validated
        domain input into the orchestration layer.

        Geography references are deliberately passed through the
        complete creation workflow:

            country_ref
            region_ref
            city_ref
        """

        return OrganizationCreationRequest(
            name=validated_data["name"],
            display_name=validated_data.get("display_name"),
            code=validated_data["code"],
            slug=validated_data["slug"],
            category=validated_data.get("category"),
            organization_type=validated_data["organization_type"],
            size=validated_data.get("size"),
            email=validated_data.get("email"),
            support_email=validated_data.get("support_email"),
            phone=validated_data.get("phone"),
            website=validated_data.get("website"),
            address=validated_data.get("address"),
            city=validated_data.get("city"),
            state=validated_data.get("state"),
            country=validated_data.get("country"),
            country_ref=validated_data.get("country_ref"),
            region_ref=validated_data.get("region_ref"),
            city_ref=validated_data.get("city_ref"),
            postal_code=validated_data.get("postal_code"),
            timezone=validated_data.get("timezone"),
            registration_number=validated_data.get(
                "registration_number",
            ),
            tax_number=validated_data.get("tax_number"),
            license_number=validated_data.get("license_number"),
            accreditation=validated_data.get("accreditation"),
            description=validated_data.get("description"),
            is_demo=validated_data.get("is_demo"),
        )

    def get_queryset(
        self,
    ) -> QuerySet[Organization]:
        """
        Return organizations visible to the current request.

        Read operations are delegated to the selector layer.
        """

        return get_organizations(
            tenant=self.current_tenant,
        )


__all__: tuple[str, ...] = ("OrganizationListCreateAPIView",)

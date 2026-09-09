"""
Organization retrieve, update, and destroy API view.
"""

from __future__ import annotations

from typing import Any

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.organizations.api.organization.serializers.detail import (
    OrganizationDetailSerializer,
)
from apps.platform.organizations.api.organization.serializers.update import (
    OrganizationUpdateSerializer,
)
from apps.platform.organizations.models import Organization
from apps.platform.organizations.permissions import (
    CanDeleteOrganization,
    CanUpdateOrganization,
    CanViewOrganization,
)
from apps.platform.organizations.selectors.organization import (
    get_organization_by_id,
)
from apps.platform.organizations.services.organization import (
    delete_organization,
    update_organization,
)
from apps.platform.organizations.workflows.organization_update import (
    OrganizationUpdateRequest,
    OrganizationUpdateWorkflow,
)


class OrganizationRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, and archive an organization.

    Update operations are workflow-driven. The workflow owns orchestration,
    authorization, domain-event publication, and post-commit tasks, while
    the service layer remains responsible for business rules and persistence.

    Geography references are passed through the complete update workflow:

        country_ref
        region_ref
        city_ref

    PATCH field presence is preserved so that an omitted nullable field is
    different from an explicitly supplied null value.
    """

    lookup_url_kwarg = "organization_id"

    permission_classes_map = {
        "GET": (CanViewOrganization,),
        "PUT": (CanUpdateOrganization,),
        "PATCH": (CanUpdateOrganization,),
        "DELETE": (CanDeleteOrganization,),
    }

    serializer_classes = {
        "GET": OrganizationDetailSerializer,
        "PUT": OrganizationUpdateSerializer,
        "PATCH": OrganizationUpdateSerializer,
    }

    detail_serializer_class = OrganizationDetailSerializer

    update_workflow = OrganizationUpdateWorkflow

    # Compatibility fallback.
    #
    # Base UpdateServiceMixin executes the workflow whenever
    # update_workflow is configured. This service remains available
    # for direct/non-workflow callers and preserves the existing
    # service-layer contract.
    update_service = staticmethod(
        update_organization,
    )

    delete_service = staticmethod(
        delete_organization,
    )

    update_success_message = "Organization updated successfully."

    delete_success_message = "Organization archived successfully."

    def get_object(
        self,
    ) -> Organization:
        """
        Return the organization requested by the URL.

        Retrieval is delegated to the selector layer.
        """

        return get_organization_by_id(
            organization_id=self.kwargs[self.lookup_url_kwarg],
        )

    def build_update_workflow_request(
        self,
        instance: Organization,
        validated_data: dict[str, Any],
    ) -> OrganizationUpdateRequest:
        """
        Build the workflow request from serializer data.

        ``validated_data`` contains only fields supplied by the client.

        This distinction is important for PATCH semantics:

        - omitted field -> absent from ``validated_data``
        - explicit ``null`` -> present with value ``None``
        - supplied value -> present with the supplied value

        The original field presence is stored in workflow metadata so the
        workflow can preserve this distinction without coupling itself to
        DRF request objects.

        The instance is used only for the stable organization identifier.
        Tenant resolution and authorization remain inside the workflow
        execution context.
        """

        return OrganizationUpdateRequest(
            organization_id=instance.id,
            name=validated_data.get("name"),
            display_name=validated_data.get("display_name"),
            category=validated_data.get("category"),
            organization_type=validated_data.get(
                "organization_type",
            ),
            status=validated_data.get("status"),
            size=validated_data.get("size"),
            email=validated_data.get("email"),
            support_email=validated_data.get(
                "support_email",
            ),
            phone=validated_data.get("phone"),
            website=validated_data.get("website"),
            address=validated_data.get("address"),
            city=validated_data.get("city"),
            state=validated_data.get("state"),
            country=validated_data.get("country"),
            country_ref=validated_data.get(
                "country_ref",
            ),
            region_ref=validated_data.get(
                "region_ref",
            ),
            city_ref=validated_data.get(
                "city_ref",
            ),
            postal_code=validated_data.get(
                "postal_code",
            ),
            timezone=validated_data.get("timezone"),
            registration_number=validated_data.get(
                "registration_number",
            ),
            tax_number=validated_data.get(
                "tax_number",
            ),
            license_number=validated_data.get(
                "license_number",
            ),
            accreditation=validated_data.get(
                "accreditation",
            ),
            description=validated_data.get(
                "description",
            ),
            is_demo=validated_data.get(
                "is_demo",
            ),
            metadata={
                "_provided_fields": tuple(
                    validated_data.keys(),
                ),
            },
        )


__all__: tuple[str, ...] = ("OrganizationRetrieveUpdateDestroyAPIView",)

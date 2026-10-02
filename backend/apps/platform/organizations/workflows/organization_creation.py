"""
Organization creation workflow.

Coordinates the organization creation process.

The workflow is responsible for:

- Policy validation
- Domain service orchestration
- Domain event publishing
- Background task scheduling

Business rules remain inside the domain service layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.platform.organizations.events import (
    OrganizationCreatedEvent,
)
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    create_organization,
)
from apps.platform.organizations.tasks import (
    index_organization,
    send_organization_created_notification,
    synchronize_organization,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationCreationRequest:
    """
    Organization creation request.

    This DTO mirrors the writable Organization creation API contract.
    Validation and normalization are performed by the serializer before
    this request reaches the workflow.
    """

    name: str
    code: str
    slug: str
    organization_type: str

    display_name: str | None = None
    category: str | None = None
    size: str | None = None

    email: str | None = None
    support_email: str | None = None
    phone: str | None = None
    website: str | None = None

    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None

    country_ref: Any | None = None
    region_ref: Any | None = None
    city_ref: Any | None = None

    postal_code: str | None = None
    timezone: str | None = None

    registration_number: str | None = None
    tax_number: str | None = None
    license_number: str | None = None
    accreditation: str | None = None

    description: str | None = None
    is_demo: bool | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationCreationData:
    """
    Organization creation workflow payload.
    """

    organization_id: UUID
    created: bool
    event_id: UUID | None = None


class OrganizationCreationWorkflow(
    BaseWorkflow[OrganizationCreationData],
):
    """
    Coordinates organization creation.

    Responsibilities:

    - Validate creation policy
    - Execute organization creation service
    - Publish organization created event
    - Dispatch post-commit tasks

    Business validation remains in the serializer/service layers.
    """

    def __init__(
        self,
        *,
        request: OrganizationCreationRequest,
        policy: OrganizationPolicy | None = None,
    ) -> None:
        super().__init__()

        self._request = request
        self._policy = policy or OrganizationPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationCreationData]:
        """
        Execute organization creation orchestration.
        """

        from apps.platform.accounts.models import User
        from apps.platform.tenancy.models import Tenant

        actor = User.objects.get(
            id=context.actor_id,
        )

        if not self._policy.can_create(
            actor=actor,
        ):
            raise PermissionError(
                "User does not have permission to create organization.",
            )

        tenant = Tenant.objects.get(
            id=context.tenant_id,
        )

        validated_data: dict[str, Any] = {
            "tenant": tenant,
            "name": self._request.name,
            "code": self._request.code,
            "slug": self._request.slug,
            "organization_type": self._request.organization_type,
        }

        optional_fields = (
            "display_name",
            "category",
            "size",
            "email",
            "support_email",
            "phone",
            "website",
            "address",
            "city",
            "state",
            "country",
            "country_ref",
            "region_ref",
            "city_ref",
            "postal_code",
            "timezone",
            "registration_number",
            "tax_number",
            "license_number",
            "accreditation",
            "description",
            "is_demo",
        )

        request_values = {
            field_name: getattr(
                self._request,
                field_name,
            )
            for field_name in optional_fields
        }

        validated_data.update(
            {
                field_name: value
                for field_name, value in request_values.items()
                if value is not None
            },
        )

        organization = create_organization(
            validated_data=validated_data,
        )

        event = OrganizationCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            organization_id=organization.id,
            organization_code=organization.code,
            organization_name=organization.name,
            organization_type=organization.organization_type,
            organization_category=organization.category,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            send_organization_created_notification,
            organization_id=organization.id,
        )

        self.dispatch_after_commit(
            index_organization,
            organization_id=organization.id,
        )

        self.dispatch_after_commit(
            synchronize_organization,
            organization_id=organization.id,
        )

        return WorkflowResult.ok(
            context=context,
            data=OrganizationCreationData(
                organization_id=organization.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Organization created successfully.",
            code="organization_created",
        )


__all__: tuple[str, ...] = (
    "OrganizationCreationRequest",
    "OrganizationCreationData",
    "OrganizationCreationWorkflow",
)

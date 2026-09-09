"""
Organization update workflow.

Coordinates organization update operations by orchestrating policies,
domain services, domain events, and background tasks.

Business rules belong in the service layer.
Authorization belongs in the policy layer.
Persistence belongs in services/repositories.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.events import (
    OrganizationUpdatedEvent,
)
from apps.platform.organizations.models import Organization
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    update_organization,
)
from apps.platform.organizations.tasks import (
    index_organization,
    synchronize_organization,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationUpdateRequest:
    """
    Organization update workflow request.

    This DTO mirrors the Organization update API contract while keeping
    workflow orchestration independent from DRF serializers.

    Nullable fields use ``None`` for both an omitted value and an
    explicitly supplied null value. Field presence is therefore tracked
    separately by ``metadata`` when the API needs to distinguish those
    cases, particularly for nullable Geography references.
    """

    organization_id: UUID

    name: str | None = None
    display_name: str | None = None
    category: str | None = None
    organization_type: str | None = None
    status: str | None = None
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

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationUpdateData:
    """
    Organization update workflow payload.
    """

    organization_id: UUID
    updated: bool
    event_id: UUID | None = None


class OrganizationUpdateWorkflow(
    BaseWorkflow[OrganizationUpdateData],
):
    """
    Coordinates organization updates.

    Responsibilities:

    - Validate authorization policy
    - Execute organization update service
    - Publish organization updated event
    - Dispatch post-commit tasks

    Business validation remains in the serializer/service layers.
    """

    def __init__(
        self,
        *,
        request: OrganizationUpdateRequest,
        policy: OrganizationPolicy | None = None,
    ) -> None:
        super().__init__()

        self._request = request
        self._policy = policy or OrganizationPolicy()

    @property
    def request(
        self,
    ) -> OrganizationUpdateRequest:
        """
        Return workflow request.
        """

        return self._request

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationUpdateData]:
        """
        Execute organization update workflow.
        """

        request = self._request

        organization = self._get_organization(
            tenant_id=context.tenant_id,
            organization_id=request.organization_id,
        )

        actor = self._get_actor(
            actor_id=context.actor_id,
        )

        #
        # Authorization boundary.
        #
        # RBAC permission:
        # organizations.update
        #
        if not self._policy.can_update(
            actor=actor,
            organization=organization,
        ):
            return WorkflowResult.fail(
                context=context,
                code="permission_denied",
                message=("You do not have permission to update this organization."),
            )

        #
        # Partial update payload.
        #
        # The view stores the fields supplied by the API request in
        # request.metadata["_provided_fields"].
        #
        # This allows PATCH to distinguish:
        #
        #     omitted field
        #         -> leave existing value unchanged
        #
        #     explicitly supplied null
        #         -> clear the value
        #
        #     supplied value
        #         -> replace the value
        #
        provided_fields = self._provided_fields()

        field_values: dict[str, Any] = {
            "name": request.name,
            "display_name": request.display_name,
            "category": request.category,
            "organization_type": request.organization_type,
            "status": request.status,
            "size": request.size,
            "email": request.email,
            "support_email": request.support_email,
            "phone": request.phone,
            "website": request.website,
            "address": request.address,
            "city": request.city,
            "state": request.state,
            "country": request.country,
            "country_ref": request.country_ref,
            "region_ref": request.region_ref,
            "city_ref": request.city_ref,
            "postal_code": request.postal_code,
            "timezone": request.timezone,
            "registration_number": request.registration_number,
            "tax_number": request.tax_number,
            "license_number": request.license_number,
            "accreditation": request.accreditation,
            "description": request.description,
            "is_demo": request.is_demo,
        }

        validated_data = {
            field_name: field_values[field_name]
            for field_name in provided_fields
            if field_name in field_values
        }

        organization = update_organization(
            instance=organization,
            validated_data=validated_data,
        )

        event = OrganizationUpdatedEvent(
            organization_id=organization.id,
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            changed_fields=list(
                validated_data.keys(),
            ),
        )

        self.publish_after_commit(
            event,
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
            data=OrganizationUpdateData(
                organization_id=organization.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Organization updated successfully.",
            code="organization_updated",
        )

    def _provided_fields(self) -> tuple[str, ...]:
        """
        Return fields explicitly supplied by the API request.

        The view layer is responsible for capturing request-field
        presence because a workflow DTO alone cannot distinguish an
        omitted nullable field from an explicitly supplied ``None``.
        """

        provided_fields = self._request.metadata.get(
            "_provided_fields",
        )

        if provided_fields is None:
            #
            # Backward-compatible fallback for direct workflow callers.
            #
            return tuple(
                field_name
                for field_name, value in {
                    "name": self._request.name,
                    "display_name": self._request.display_name,
                    "category": self._request.category,
                    "organization_type": self._request.organization_type,
                    "status": self._request.status,
                    "size": self._request.size,
                    "email": self._request.email,
                    "support_email": self._request.support_email,
                    "phone": self._request.phone,
                    "website": self._request.website,
                    "address": self._request.address,
                    "city": self._request.city,
                    "state": self._request.state,
                    "country": self._request.country,
                    "country_ref": self._request.country_ref,
                    "region_ref": self._request.region_ref,
                    "city_ref": self._request.city_ref,
                    "postal_code": self._request.postal_code,
                    "timezone": self._request.timezone,
                    "registration_number": self._request.registration_number,
                    "tax_number": self._request.tax_number,
                    "license_number": self._request.license_number,
                    "accreditation": self._request.accreditation,
                    "description": self._request.description,
                    "is_demo": self._request.is_demo,
                }.items()
                if value is not None
            )

        if not isinstance(
            provided_fields,
            (list, tuple, set, frozenset),
        ):
            raise TypeError(
                "Organization update metadata '_provided_fields' "
                "must be a collection of field names.",
            )

        return tuple(
            field_name for field_name in provided_fields if isinstance(field_name, str)
        )

    def _get_organization(
        self,
        *,
        tenant_id: UUID,
        organization_id: UUID,
    ) -> Organization:
        """
        Load organization inside tenant boundary.
        """

        return Organization.objects.get(
            tenant_id=tenant_id,
            id=organization_id,
        )

    def _get_actor(
        self,
        *,
        actor_id: UUID,
    ) -> User:
        """
        Load workflow actor.
        """

        return User.objects.get(
            id=actor_id,
        )


__all__: tuple[str, ...] = (
    "OrganizationUpdateRequest",
    "OrganizationUpdateData",
    "OrganizationUpdateWorkflow",
)

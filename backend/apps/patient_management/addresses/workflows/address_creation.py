"""
Patient Address creation workflow.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.addresses.events import (
    AddressCreatedEvent,
)
from apps.patient_management.addresses.policies import (
    AddressPolicy,
)
from apps.patient_management.addresses.services import (
    create_address,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressCreationRequest:
    organization_id: UUID
    patient_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressCreationData:
    address_id: UUID
    created: bool
    event_id: UUID | None = None


class AddressCreationWorkflow(
    BaseWorkflow[AddressCreationData],
):
    workflow_name = "address.create"

    def __init__(
        self,
        *,
        request: AddressCreationRequest,
        policy: AddressPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or AddressPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[AddressCreationData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )

            patient = Patient.objects.get(
                pk=self._request.patient_id,
                organization_id=organization.pk,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested organization or patient was not found.",
            ) from exc

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to create an address.",
            )

        data = dict(
            self._request.data,
        )
        data["organization"] = organization
        data["patient"] = patient

        address = create_address(
            validated_data=data,
            performed_by=actor,
        )

        event = AddressCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            address_id=address.id,
            patient_id=address.patient_id,
            organization_id=address.organization_id,
            address_type=address.address_type,
            status=address.status,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=AddressCreationData(
                address_id=address.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient address created successfully.",
            code="address_created",
        )


__all__ = (
    "AddressCreationData",
    "AddressCreationRequest",
    "AddressCreationWorkflow",
)

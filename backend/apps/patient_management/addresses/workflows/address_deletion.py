"""
Patient Address deletion workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.addresses.events import (
    AddressDeletedEvent,
)
from apps.patient_management.addresses.models import Address
from apps.patient_management.addresses.policies import (
    AddressPolicy,
)
from apps.patient_management.addresses.services import (
    delete_address,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressDeletionRequest:
    address_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressDeletionData:
    address_id: UUID
    deleted: bool
    event_id: UUID


class AddressDeletionWorkflow(
    BaseWorkflow[AddressDeletionData],
):
    workflow_name = "address.delete"

    def __init__(
        self,
        *,
        request: AddressDeletionRequest,
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
    ) -> WorkflowResult[AddressDeletionData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            address = Address.objects.select_related(
                "organization",
                "patient",
            ).get(
                pk=self._request.address_id,
                organization__tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient address was not found.",
            ) from exc

        if not self._policy.can_delete(
            actor=actor,
            address=address,
        ):
            raise PermissionError(
                "User does not have permission to delete this address.",
            )

        address_id = address.id
        patient_id = address.patient_id
        organization_id = address.organization_id
        address_type = address.address_type

        delete_address(
            instance=address,
            performed_by=actor,
        )

        event = AddressDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            address_id=address_id,
            patient_id=patient_id,
            organization_id=organization_id,
            address_type=address_type,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=AddressDeletionData(
                address_id=address_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Patient address deleted successfully.",
            code="address_deleted",
        )


__all__ = (
    "AddressDeletionData",
    "AddressDeletionRequest",
    "AddressDeletionWorkflow",
)

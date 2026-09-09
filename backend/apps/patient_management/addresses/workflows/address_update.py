"""
Patient Address update workflow.
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
    AddressUpdatedEvent,
)
from apps.patient_management.addresses.models import Address
from apps.patient_management.addresses.policies import (
    AddressPolicy,
)
from apps.patient_management.addresses.services import (
    update_address,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressUpdateRequest:
    address_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressUpdateData:
    address_id: UUID
    updated: bool
    event_id: UUID | None = None


class AddressUpdateWorkflow(
    BaseWorkflow[AddressUpdateData],
):
    workflow_name = "address.update"

    def __init__(
        self,
        *,
        request: AddressUpdateRequest,
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
    ) -> WorkflowResult[AddressUpdateData]:
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
                "The requested patient address was not found.",
            ) from exc

        if not self._policy.can_update(
            actor=actor,
            address=address,
        ):
            raise PermissionError(
                "User does not have permission to update this address.",
            )

        data = dict(
            self._request.data,
        )

        if not data:
            return WorkflowResult.ok(
                context=context,
                data=AddressUpdateData(
                    address_id=address.id,
                    updated=False,
                ),
                message="No address changes were supplied.",
                code="address_unchanged",
            )

        updated = update_address(
            instance=address,
            validated_data=data,
            performed_by=actor,
        )

        event = AddressUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            address_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            address_type=updated.address_type,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=AddressUpdateData(
                address_id=updated.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient address updated successfully.",
            code="address_updated",
        )


__all__ = (
    "AddressUpdateData",
    "AddressUpdateRequest",
    "AddressUpdateWorkflow",
)

"""
Patient Address verification workflow.
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
    AddressStatusChangedEvent,
)
from apps.patient_management.addresses.models import Address
from apps.patient_management.addresses.policies import (
    AddressPolicy,
)
from apps.patient_management.addresses.services import (
    verify_address,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressVerificationRequest:
    address_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressVerificationData:
    address_id: UUID
    status: str
    verified: bool
    event_id: UUID | None = None


class AddressVerificationWorkflow(
    BaseWorkflow[AddressVerificationData],
):
    workflow_name = "address.verify"

    def __init__(
        self,
        *,
        request: AddressVerificationRequest,
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
    ) -> WorkflowResult[AddressVerificationData]:
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

        if not self._policy.can_verify(
            actor=actor,
            address=address,
        ):
            raise PermissionError(
                "User does not have permission to verify this address.",
            )

        previous_status = address.status

        updated = verify_address(
            instance=address,
            performed_by=actor,
        )

        if previous_status == updated.status:
            return WorkflowResult.ok(
                context=context,
                data=AddressVerificationData(
                    address_id=updated.id,
                    status=updated.status,
                    verified=True,
                    event_id=None,
                ),
                message="Patient address is already verified.",
                code="address_already_verified",
            )

        event = AddressStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            address_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_status=previous_status,
            new_status=updated.status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=AddressVerificationData(
                address_id=updated.id,
                status=updated.status,
                verified=True,
                event_id=event.event_id,
            ),
            message="Patient address verified successfully.",
            code="address_verified",
        )


__all__ = (
    "AddressVerificationData",
    "AddressVerificationRequest",
    "AddressVerificationWorkflow",
)

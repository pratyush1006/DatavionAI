"""
Patient Address lifecycle workflows.
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
    AddressPrimaryChangedEvent,
    AddressStatusChangedEvent,
)
from apps.patient_management.addresses.models import Address
from apps.patient_management.addresses.policies import (
    AddressPolicy,
)
from apps.patient_management.addresses.services import (
    activate_address,
    deactivate_address,
    set_primary_address,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressActivationRequest:
    address_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressDeactivationRequest:
    address_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressPrimaryRequest:
    address_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressLifecycleData:
    address_id: UUID
    status: str
    changed: bool
    event_id: UUID | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AddressPrimaryData:
    address_id: UUID
    patient_id: UUID
    address_type: str
    is_primary: bool
    event_id: UUID | None = None


def _get_address(
    *,
    address_id: UUID,
    tenant_id: UUID,
) -> Address:
    return Address.objects.select_related(
        "organization",
        "patient",
    ).get(
        pk=address_id,
        organization__tenant_id=tenant_id,
    )


class AddressActivationWorkflow(
    BaseWorkflow[AddressLifecycleData],
):
    workflow_name = "address.activate"

    def __init__(
        self,
        *,
        request: AddressActivationRequest,
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
    ) -> WorkflowResult[AddressLifecycleData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            address = _get_address(
                address_id=self._request.address_id,
                tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient address was not found.",
            ) from exc

        if not self._policy.can_activate(
            actor=actor,
            address=address,
        ):
            raise PermissionError(
                "User does not have permission to activate this address.",
            )

        previous_status = address.status

        updated = activate_address(
            instance=address,
            performed_by=actor,
        )

        if previous_status == updated.status:
            return WorkflowResult.ok(
                context=context,
                data=AddressLifecycleData(
                    address_id=updated.id,
                    status=updated.status,
                    changed=False,
                ),
                message="Patient address is already active.",
                code="address_unchanged",
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
            data=AddressLifecycleData(
                address_id=updated.id,
                status=updated.status,
                changed=True,
                event_id=event.event_id,
            ),
            message="Patient address activated successfully.",
            code="address_activated",
        )


class AddressDeactivationWorkflow(
    BaseWorkflow[AddressLifecycleData],
):
    workflow_name = "address.deactivate"

    def __init__(
        self,
        *,
        request: AddressDeactivationRequest,
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
    ) -> WorkflowResult[AddressLifecycleData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            address = _get_address(
                address_id=self._request.address_id,
                tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient address was not found.",
            ) from exc

        if not self._policy.can_deactivate(
            actor=actor,
            address=address,
        ):
            raise PermissionError(
                "User does not have permission to deactivate this address.",
            )

        previous_status = address.status
        previous_primary = address.is_primary

        updated = deactivate_address(
            instance=address,
            performed_by=actor,
        )

        status_event = AddressStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            address_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_status=previous_status,
            new_status=updated.status,
        )

        self.publish_after_commit(status_event)

        event_id = status_event.event_id

        if previous_primary:
            primary_event = AddressPrimaryChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                address_id=updated.id,
                patient_id=updated.patient_id,
                organization_id=updated.organization_id,
                address_type=updated.address_type,
                previous_primary=True,
                new_primary=False,
            )

            self.publish_after_commit(primary_event)
            event_id = primary_event.event_id

        return WorkflowResult.ok(
            context=context,
            data=AddressLifecycleData(
                address_id=updated.id,
                status=updated.status,
                changed=True,
                event_id=event_id,
            ),
            message="Patient address deactivated successfully.",
            code="address_deactivated",
        )


class AddressPrimaryWorkflow(
    BaseWorkflow[AddressPrimaryData],
):
    workflow_name = "address.set_primary"

    def __init__(
        self,
        *,
        request: AddressPrimaryRequest,
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
    ) -> WorkflowResult[AddressPrimaryData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            address = _get_address(
                address_id=self._request.address_id,
                tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient address was not found.",
            ) from exc

        if not self._policy.can_set_primary(
            actor=actor,
            address=address,
        ):
            raise PermissionError(
                "User does not have permission to set this address as primary.",
            )

        previous_primary = address.is_primary

        updated = set_primary_address(
            instance=address,
            performed_by=actor,
        )

        if previous_primary:
            return WorkflowResult.ok(
                context=context,
                data=AddressPrimaryData(
                    address_id=updated.id,
                    patient_id=updated.patient_id,
                    address_type=updated.address_type,
                    is_primary=True,
                    event_id=None,
                ),
                message="Patient address is already primary.",
                code="address_primary_unchanged",
            )

        event = AddressPrimaryChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            address_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            address_type=updated.address_type,
            previous_primary=False,
            new_primary=True,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=AddressPrimaryData(
                address_id=updated.id,
                patient_id=updated.patient_id,
                address_type=updated.address_type,
                is_primary=True,
                event_id=event.event_id,
            ),
            message="Patient address set as primary successfully.",
            code="address_primary_changed",
        )


__all__ = (
    "AddressActivationRequest",
    "AddressActivationWorkflow",
    "AddressDeactivationRequest",
    "AddressDeactivationWorkflow",
    "AddressLifecycleData",
    "AddressPrimaryData",
    "AddressPrimaryRequest",
    "AddressPrimaryWorkflow",
)

"""
Emergency Contact lifecycle workflows.

Includes:
- activation
- deactivation
- blocking
- set primary
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
from apps.patient_management.emergency_contacts.events import (
    EmergencyContactPrimaryChangedEvent,
    EmergencyContactStatusChangedEvent,
)
from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)
from apps.patient_management.emergency_contacts.policies import (
    EmergencyContactPolicy,
)
from apps.patient_management.emergency_contacts.services import (
    activate_emergency_contact,
    block_emergency_contact,
    deactivate_emergency_contact,
    set_primary_emergency_contact,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactActivationRequest:
    emergency_contact_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactDeactivationRequest:
    emergency_contact_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactBlockRequest:
    emergency_contact_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactPrimaryRequest:
    emergency_contact_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactLifecycleData:
    emergency_contact_id: UUID
    status: str
    changed: bool
    event_id: UUID | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactPrimaryData:
    emergency_contact_id: UUID
    patient_id: UUID
    is_primary: bool
    changed: bool
    event_id: UUID | None = None


def _get_emergency_contact(
    *,
    emergency_contact_id: UUID,
    tenant_id: UUID,
) -> EmergencyContact:
    return EmergencyContact.objects.select_related(
        "organization",
        "patient",
    ).get(
        pk=emergency_contact_id,
        organization__tenant_id=tenant_id,
    )


class EmergencyContactActivationWorkflow(
    BaseWorkflow[EmergencyContactLifecycleData],
):
    workflow_name = "emergency_contact.activate"

    def __init__(
        self,
        *,
        request: EmergencyContactActivationRequest,
        policy: EmergencyContactPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or EmergencyContactPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[EmergencyContactLifecycleData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            emergency_contact = _get_emergency_contact(
                emergency_contact_id=self._request.emergency_contact_id,
                tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Emergency contact was not found.",
            ) from exc

        if not self._policy.can_activate(
            actor=actor,
            emergency_contact=emergency_contact,
        ):
            raise PermissionError(
                "User does not have permission to activate this emergency contact.",
            )

        previous_status = emergency_contact.status

        updated = activate_emergency_contact(
            instance=emergency_contact,
            performed_by=actor,
        )

        if previous_status == updated.status:
            return WorkflowResult.ok(
                context=context,
                data=EmergencyContactLifecycleData(
                    emergency_contact_id=updated.id,
                    status=updated.status,
                    changed=False,
                ),
                message="Emergency contact is already active.",
                code="emergency_contact_activation_unchanged",
            )

        event = EmergencyContactStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            emergency_contact_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_status=previous_status,
            new_status=updated.status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=EmergencyContactLifecycleData(
                emergency_contact_id=updated.id,
                status=updated.status,
                changed=True,
                event_id=event.event_id,
            ),
            message="Emergency contact activated successfully.",
            code="emergency_contact_activated",
        )


class EmergencyContactDeactivationWorkflow(
    BaseWorkflow[EmergencyContactLifecycleData],
):
    workflow_name = "emergency_contact.deactivate"

    def __init__(
        self,
        *,
        request: EmergencyContactDeactivationRequest,
        policy: EmergencyContactPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or EmergencyContactPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[EmergencyContactLifecycleData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            emergency_contact = _get_emergency_contact(
                emergency_contact_id=self._request.emergency_contact_id,
                tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Emergency contact was not found.",
            ) from exc

        if not self._policy.can_deactivate(
            actor=actor,
            emergency_contact=emergency_contact,
        ):
            raise PermissionError(
                "User does not have permission to deactivate this emergency contact.",
            )

        previous_status = emergency_contact.status
        previous_primary = emergency_contact.is_primary

        updated = deactivate_emergency_contact(
            instance=emergency_contact,
            performed_by=actor,
        )

        status_event = EmergencyContactStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            emergency_contact_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_status=previous_status,
            new_status=updated.status,
        )

        self.publish_after_commit(status_event)

        event_id = status_event.event_id

        if previous_primary:
            primary_event = EmergencyContactPrimaryChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                emergency_contact_id=updated.id,
                patient_id=updated.patient_id,
                organization_id=updated.organization_id,
                previous_primary=True,
                new_primary=False,
            )

            self.publish_after_commit(primary_event)

            event_id = primary_event.event_id

        return WorkflowResult.ok(
            context=context,
            data=EmergencyContactLifecycleData(
                emergency_contact_id=updated.id,
                status=updated.status,
                changed=(previous_status != updated.status or previous_primary),
                event_id=event_id,
            ),
            message="Emergency contact deactivated successfully.",
            code="emergency_contact_deactivated",
        )


class EmergencyContactBlockWorkflow(
    BaseWorkflow[EmergencyContactLifecycleData],
):
    workflow_name = "emergency_contact.block"

    def __init__(
        self,
        *,
        request: EmergencyContactBlockRequest,
        policy: EmergencyContactPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or EmergencyContactPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[EmergencyContactLifecycleData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            emergency_contact = _get_emergency_contact(
                emergency_contact_id=self._request.emergency_contact_id,
                tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Emergency contact was not found.",
            ) from exc

        if not self._policy.can_block(
            actor=actor,
            emergency_contact=emergency_contact,
        ):
            raise PermissionError(
                "User does not have permission to block this emergency contact.",
            )

        previous_status = emergency_contact.status
        previous_primary = emergency_contact.is_primary

        updated = block_emergency_contact(
            instance=emergency_contact,
            performed_by=actor,
        )

        status_event = EmergencyContactStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            emergency_contact_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_status=previous_status,
            new_status=updated.status,
        )

        self.publish_after_commit(status_event)

        event_id = status_event.event_id

        if previous_primary:
            primary_event = EmergencyContactPrimaryChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                emergency_contact_id=updated.id,
                patient_id=updated.patient_id,
                organization_id=updated.organization_id,
                previous_primary=True,
                new_primary=False,
            )

            self.publish_after_commit(primary_event)

            event_id = primary_event.event_id

        return WorkflowResult.ok(
            context=context,
            data=EmergencyContactLifecycleData(
                emergency_contact_id=updated.id,
                status=updated.status,
                changed=True,
                event_id=event_id,
            ),
            message="Emergency contact blocked successfully.",
            code="emergency_contact_blocked",
        )


class EmergencyContactPrimaryWorkflow(
    BaseWorkflow[EmergencyContactPrimaryData],
):
    workflow_name = "emergency_contact.set_primary"

    def __init__(
        self,
        *,
        request: EmergencyContactPrimaryRequest,
        policy: EmergencyContactPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or EmergencyContactPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[EmergencyContactPrimaryData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            emergency_contact = _get_emergency_contact(
                emergency_contact_id=self._request.emergency_contact_id,
                tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Emergency contact was not found.",
            ) from exc

        if not self._policy.can_set_primary(
            actor=actor,
            emergency_contact=emergency_contact,
        ):
            raise PermissionError(
                "User does not have permission to set this emergency contact as primary.",
            )

        previous_primary = emergency_contact.is_primary

        updated = set_primary_emergency_contact(
            instance=emergency_contact,
            performed_by=actor,
        )

        if previous_primary:
            return WorkflowResult.ok(
                context=context,
                data=EmergencyContactPrimaryData(
                    emergency_contact_id=updated.id,
                    patient_id=updated.patient_id,
                    is_primary=True,
                    changed=False,
                ),
                message="Emergency contact is already primary.",
                code="emergency_contact_primary_unchanged",
            )

        event = EmergencyContactPrimaryChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            emergency_contact_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_primary=False,
            new_primary=True,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=EmergencyContactPrimaryData(
                emergency_contact_id=updated.id,
                patient_id=updated.patient_id,
                is_primary=True,
                changed=True,
                event_id=event.event_id,
            ),
            message="Emergency contact set as primary successfully.",
            code="emergency_contact_primary_changed",
        )


__all__ = (
    "EmergencyContactActivationRequest",
    "EmergencyContactActivationWorkflow",
    "EmergencyContactBlockRequest",
    "EmergencyContactBlockWorkflow",
    "EmergencyContactDeactivationRequest",
    "EmergencyContactDeactivationWorkflow",
    "EmergencyContactLifecycleData",
    "EmergencyContactPrimaryData",
    "EmergencyContactPrimaryRequest",
    "EmergencyContactPrimaryWorkflow",
)

"""
Patient Contact lifecycle workflows.

Includes:
- Activation
- Deactivation
- Set primary
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
from apps.patient_management.contacts.events import (
    ContactPrimaryChangedEvent,
    ContactStatusChangedEvent,
)
from apps.patient_management.contacts.models import Contact
from apps.patient_management.contacts.policies import (
    ContactPolicy,
)
from apps.patient_management.contacts.services import (
    activate_contact,
    deactivate_contact,
    set_primary_contact,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactActivationRequest:
    contact_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactDeactivationRequest:
    contact_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactPrimaryRequest:
    contact_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactLifecycleData:
    contact_id: UUID
    status: str
    changed: bool
    event_id: UUID | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactPrimaryData:
    contact_id: UUID
    patient_id: UUID
    contact_type: str
    is_primary: bool
    event_id: UUID | None = None


def _get_contact(
    *,
    contact_id: UUID,
    tenant_id: UUID,
) -> Contact:
    contact: Contact = Contact.objects.select_related(
        "organization",
        "patient",
    ).get(
        pk=contact_id,
        organization__tenant_id=tenant_id,
    )
    return contact


class ContactActivationWorkflow(
    BaseWorkflow[ContactLifecycleData],
):
    workflow_name = "contact.activate"

    def __init__(
        self,
        *,
        request: ContactActivationRequest,
        policy: ContactPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or ContactPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[ContactLifecycleData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            contact = _get_contact(
                contact_id=self._request.contact_id,
                tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient contact was not found.",
            ) from exc

        if not self._policy.can_activate(
            actor=actor,
            contact=contact,
        ):
            raise PermissionError(
                "User does not have permission to activate this patient contact.",
            )

        previous_status = contact.status

        updated = activate_contact(
            instance=contact,
            performed_by=actor,
        )

        if previous_status == updated.status:
            return WorkflowResult.ok(
                context=context,
                data=ContactLifecycleData(
                    contact_id=updated.id,
                    status=updated.status,
                    changed=False,
                ),
                message="Patient contact is already active.",
                code="contact_unchanged",
            )

        patient_id: UUID = updated.patient.pk
        organization_id: UUID = updated.organization.pk

        event = ContactStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            contact_id=updated.id,
            patient_id=patient_id,
            organization_id=organization_id,
            previous_status=previous_status,
            new_status=updated.status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=ContactLifecycleData(
                contact_id=updated.id,
                status=updated.status,
                changed=True,
                event_id=event.event_id,
            ),
            message="Patient contact activated successfully.",
            code="contact_activated",
        )


class ContactDeactivationWorkflow(
    BaseWorkflow[ContactLifecycleData],
):
    workflow_name = "contact.deactivate"

    def __init__(
        self,
        *,
        request: ContactDeactivationRequest,
        policy: ContactPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or ContactPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[ContactLifecycleData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            contact = _get_contact(
                contact_id=self._request.contact_id,
                tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient contact was not found.",
            ) from exc

        if not self._policy.can_deactivate(
            actor=actor,
            contact=contact,
        ):
            raise PermissionError(
                "User does not have permission to deactivate this patient contact.",
            )

        previous_status = contact.status
        previous_primary = contact.is_primary

        updated = deactivate_contact(
            instance=contact,
            performed_by=actor,
        )

        patient_id: UUID = updated.patient.pk
        organization_id: UUID = updated.organization.pk

        status_event = ContactStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            contact_id=updated.id,
            patient_id=patient_id,
            organization_id=organization_id,
            previous_status=previous_status,
            new_status=updated.status,
        )

        self.publish_after_commit(status_event)

        event_id = status_event.event_id

        if previous_primary:
            primary_event = ContactPrimaryChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                contact_id=updated.id,
                patient_id=patient_id,
                organization_id=organization_id,
                contact_type=updated.contact_type,
                previous_primary=True,
                new_primary=False,
            )

            self.publish_after_commit(primary_event)
            event_id = primary_event.event_id

        return WorkflowResult.ok(
            context=context,
            data=ContactLifecycleData(
                contact_id=updated.id,
                status=updated.status,
                changed=True,
                event_id=event_id,
            ),
            message="Patient contact deactivated successfully.",
            code="contact_deactivated",
        )


class ContactPrimaryWorkflow(
    BaseWorkflow[ContactPrimaryData],
):
    workflow_name = "contact.set_primary"

    def __init__(
        self,
        *,
        request: ContactPrimaryRequest,
        policy: ContactPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or ContactPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[ContactPrimaryData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            contact = _get_contact(
                contact_id=self._request.contact_id,
                tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient contact was not found.",
            ) from exc

        if not self._policy.can_set_primary(
            actor=actor,
            contact=contact,
        ):
            raise PermissionError(
                "User does not have permission to set this patient contact as primary.",
            )

        previous_primary = contact.is_primary

        updated = set_primary_contact(
            instance=contact,
            performed_by=actor,
        )

        patient_id: UUID = updated.patient.pk
        organization_id: UUID = updated.organization.pk

        if previous_primary:
            return WorkflowResult.ok(
                context=context,
                data=ContactPrimaryData(
                    contact_id=updated.id,
                    patient_id=patient_id,
                    contact_type=updated.contact_type,
                    is_primary=True,
                    event_id=None,
                ),
                message="Patient contact is already primary.",
                code="contact_primary_unchanged",
            )

        event = ContactPrimaryChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            contact_id=updated.id,
            patient_id=patient_id,
            organization_id=organization_id,
            contact_type=updated.contact_type,
            previous_primary=False,
            new_primary=True,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=ContactPrimaryData(
                contact_id=updated.id,
                patient_id=patient_id,
                contact_type=updated.contact_type,
                is_primary=True,
                event_id=event.event_id,
            ),
            message="Patient contact set as primary successfully.",
            code="contact_primary_changed",
        )


__all__ = (
    "ContactActivationRequest",
    "ContactActivationWorkflow",
    "ContactDeactivationRequest",
    "ContactDeactivationWorkflow",
    "ContactLifecycleData",
    "ContactPrimaryData",
    "ContactPrimaryRequest",
    "ContactPrimaryWorkflow",
)

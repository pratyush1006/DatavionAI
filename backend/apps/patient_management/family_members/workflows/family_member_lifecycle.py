"""
Patient Family Member lifecycle workflows.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.family_members.events import (
    FamilyMemberPrimaryChangedEvent,
    FamilyMemberStatusChangedEvent,
)
from apps.patient_management.family_members.models import FamilyMember
from apps.patient_management.family_members.policies import FamilyMemberPolicy
from apps.patient_management.family_members.services import FamilyMemberService
from apps.platform.accounts.models import User

# ============================================================================
# Requests
# ============================================================================


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberActivationRequest:
    family_member_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberDeactivationRequest:
    family_member_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberRestoreRequest:
    family_member_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberNextOfKinRequest:
    family_member_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberEmergencyContactRequest:
    family_member_id: UUID


# ============================================================================
# Results
# ============================================================================


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberActivationData:
    family_member_id: UUID
    status: str
    changed: bool
    event_id: UUID | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberDeactivationData:
    family_member_id: UUID
    status: str
    changed: bool
    event_id: UUID | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberRestoreData:
    family_member_id: UUID
    restored: bool
    status: str
    event_id: UUID | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberNextOfKinData:
    family_member_id: UUID
    patient_id: UUID
    is_next_of_kin: bool
    changed: bool
    event_id: UUID | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberEmergencyContactData:
    family_member_id: UUID
    patient_id: UUID
    is_emergency_contact: bool
    changed: bool
    event_id: UUID | None = None


# ============================================================================
# Internal base
# ============================================================================


class _FamilyMemberLifecycleWorkflow(BaseWorkflow):
    policy_method: str

    def __init__(self, *, request, policy=None, logger_=None) -> None:
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or FamilyMemberPolicy()

    def _get(self, context: WorkflowContext, *, deleted=False):
        manager = FamilyMember.deleted_objects if deleted else FamilyMember.objects

        try:
            return (
                User.objects.get(pk=context.actor_id),
                manager.select_related("organization", "patient").get(
                    pk=self._request.family_member_id,
                    organization__tenant_id=context.tenant_id,
                ),
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient family member was not found.",
            ) from exc

    def _allowed(self, actor, member) -> bool:
        return getattr(self._policy, self.policy_method)(
            actor=actor,
            family_member=member,
        )

    def _error(self, action: str) -> PermissionError:
        return PermissionError(
            f"User does not have permission to {action} this patient family member.",
        )


# ============================================================================
# Status lifecycle
# ============================================================================


class FamilyMemberActivationWorkflow(
    _FamilyMemberLifecycleWorkflow,
):
    workflow_name = "family_member.activate"
    policy_method = "can_activate"

    @transaction.atomic
    def _run(self, context):
        actor, member = self._get(context)

        if not self._allowed(actor, member):
            raise self._error("activate")

        previous = member.status
        member = FamilyMemberService.activate(
            instance=member,
            performed_by=actor,
        )

        changed = previous != member.status
        event = (
            FamilyMemberStatusChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                family_member_id=member.id,
                patient_id=member.patient_id,
                organization_id=member.organization_id,
                previous_status=previous,
                new_status=member.status,
            )
            if changed
            else None
        )

        if event:
            self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=FamilyMemberActivationData(
                family_member_id=member.id,
                status=member.status,
                changed=changed,
                event_id=event.event_id if event else None,
            ),
            message=(
                "Patient family member activated successfully."
                if changed
                else "Patient family member is already active."
            ),
            code=("family_member_activated" if changed else "family_member_unchanged"),
        )


class FamilyMemberDeactivationWorkflow(
    _FamilyMemberLifecycleWorkflow,
):
    workflow_name = "family_member.deactivate"
    policy_method = "can_deactivate"

    @transaction.atomic
    def _run(self, context):
        actor, member = self._get(context)

        if not self._allowed(actor, member):
            raise self._error("deactivate")

        previous = member.status
        previous_next_of_kin = member.is_next_of_kin
        previous_emergency = member.is_emergency_contact

        member = FamilyMemberService.deactivate(
            instance=member,
            performed_by=actor,
        )

        events = []

        if previous != member.status:
            events.append(
                FamilyMemberStatusChangedEvent(
                    tenant_id=context.tenant_id,
                    actor_id=context.actor_id,
                    family_member_id=member.id,
                    patient_id=member.patient_id,
                    organization_id=member.organization_id,
                    previous_status=previous,
                    new_status=member.status,
                )
            )

        if previous_next_of_kin != member.is_next_of_kin:
            events.append(
                FamilyMemberPrimaryChangedEvent(
                    tenant_id=context.tenant_id,
                    actor_id=context.actor_id,
                    family_member_id=member.id,
                    patient_id=member.patient_id,
                    organization_id=member.organization_id,
                    flag="next_of_kin",
                    previous_value=previous_next_of_kin,
                    new_value=member.is_next_of_kin,
                )
            )

        if previous_emergency != member.is_emergency_contact:
            events.append(
                FamilyMemberPrimaryChangedEvent(
                    tenant_id=context.tenant_id,
                    actor_id=context.actor_id,
                    family_member_id=member.id,
                    patient_id=member.patient_id,
                    organization_id=member.organization_id,
                    flag="emergency_contact",
                    previous_value=previous_emergency,
                    new_value=member.is_emergency_contact,
                )
            )

        for event in events:
            self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=FamilyMemberDeactivationData(
                family_member_id=member.id,
                status=member.status,
                changed=bool(events),
                event_id=events[-1].event_id if events else None,
            ),
            message=(
                "Patient family member deactivated successfully."
                if events
                else "Patient family member is already inactive."
            ),
            code=("family_member_deactivated" if events else "family_member_unchanged"),
        )


# ============================================================================
# Restore
# ============================================================================


class FamilyMemberRestoreWorkflow(
    _FamilyMemberLifecycleWorkflow,
):
    workflow_name = "family_member.restore"
    policy_method = "can_restore"

    @transaction.atomic
    def _run(self, context):
        actor, member = self._get(context, deleted=True)

        if not self._allowed(actor, member):
            raise self._error("restore")

        member = FamilyMemberService.restore(
            instance=member,
            performed_by=actor,
        )

        return WorkflowResult.ok(
            context=context,
            data=FamilyMemberRestoreData(
                family_member_id=member.id,
                restored=True,
                status=member.status,
            ),
            message="Patient family member restored successfully.",
            code="family_member_restored",
        )


# ============================================================================
# Flag lifecycle
# ============================================================================


class FamilyMemberNextOfKinWorkflow(
    _FamilyMemberLifecycleWorkflow,
):
    workflow_name = "family_member.set_next_of_kin"
    policy_method = "can_manage_next_of_kin"

    @transaction.atomic
    def _run(self, context):
        actor, member = self._get(context)

        if not self._allowed(actor, member):
            raise self._error("manage the patient's next of kin")

        previous = member.is_next_of_kin
        member = FamilyMemberService.mark_next_of_kin(
            instance=member,
            performed_by=actor,
        )

        changed = previous != member.is_next_of_kin
        event = (
            FamilyMemberPrimaryChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                family_member_id=member.id,
                patient_id=member.patient_id,
                organization_id=member.organization_id,
                flag="next_of_kin",
                previous_value=previous,
                new_value=member.is_next_of_kin,
            )
            if changed
            else None
        )

        if event:
            self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=FamilyMemberNextOfKinData(
                family_member_id=member.id,
                patient_id=member.patient_id,
                is_next_of_kin=member.is_next_of_kin,
                changed=changed,
                event_id=event.event_id if event else None,
            ),
            message=(
                "Patient family member set as next of kin successfully."
                if changed
                else "Patient family member is already next of kin."
            ),
            code=(
                "family_member_next_of_kin_changed"
                if changed
                else "family_member_unchanged"
            ),
        )


class FamilyMemberEmergencyContactWorkflow(
    _FamilyMemberLifecycleWorkflow,
):
    workflow_name = "family_member.set_emergency_contact"
    policy_method = "can_manage_emergency_contact"

    @transaction.atomic
    def _run(self, context):
        actor, member = self._get(context)

        if not self._allowed(actor, member):
            raise self._error(
                "manage the patient's emergency contacts",
            )

        previous = member.is_emergency_contact
        member = FamilyMemberService.mark_emergency_contact(
            instance=member,
            performed_by=actor,
        )

        changed = previous != member.is_emergency_contact
        event = (
            FamilyMemberPrimaryChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                family_member_id=member.id,
                patient_id=member.patient_id,
                organization_id=member.organization_id,
                flag="emergency_contact",
                previous_value=previous,
                new_value=member.is_emergency_contact,
            )
            if changed
            else None
        )

        if event:
            self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=FamilyMemberEmergencyContactData(
                family_member_id=member.id,
                patient_id=member.patient_id,
                is_emergency_contact=member.is_emergency_contact,
                changed=changed,
                event_id=event.event_id if event else None,
            ),
            message=(
                "Patient family member set as emergency contact successfully."
                if changed
                else "Patient family member is already an emergency contact."
            ),
            code=(
                "family_member_emergency_contact_changed"
                if changed
                else "family_member_unchanged"
            ),
        )


__all__ = (
    "FamilyMemberActivationRequest",
    "FamilyMemberActivationData",
    "FamilyMemberActivationWorkflow",
    "FamilyMemberDeactivationRequest",
    "FamilyMemberDeactivationData",
    "FamilyMemberDeactivationWorkflow",
    "FamilyMemberRestoreRequest",
    "FamilyMemberRestoreData",
    "FamilyMemberRestoreWorkflow",
    "FamilyMemberNextOfKinRequest",
    "FamilyMemberNextOfKinData",
    "FamilyMemberNextOfKinWorkflow",
    "FamilyMemberEmergencyContactRequest",
    "FamilyMemberEmergencyContactData",
    "FamilyMemberEmergencyContactWorkflow",
)

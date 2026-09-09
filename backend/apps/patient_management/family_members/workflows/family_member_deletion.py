"""
Patient Family Member deletion workflow.

Canonical mutation flow:
API → Workflow → Policy → Service → Domain Event
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.family_members.events import FamilyMemberDeletedEvent
from apps.patient_management.family_members.models import FamilyMember
from apps.patient_management.family_members.policies import FamilyMemberPolicy
from apps.patient_management.family_members.services import FamilyMemberService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberDeletionRequest:
    family_member_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberDeletionData:
    family_member_id: UUID
    deleted: bool
    event_id: UUID


class FamilyMemberDeletionWorkflow(
    BaseWorkflow[FamilyMemberDeletionData],
):
    """Soft-delete a tenant-scoped patient family member."""

    workflow_name = "family_member.delete"

    def __init__(
        self,
        *,
        request: FamilyMemberDeletionRequest,
        policy: FamilyMemberPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or FamilyMemberPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[FamilyMemberDeletionData]:
        try:
            actor = User.objects.get(pk=context.actor_id)
            member = FamilyMember.objects.select_related("organization", "patient").get(
                pk=self._request.family_member_id,
                organization__tenant_id=context.tenant_id,
                is_deleted=False,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient family member was not found.",
            ) from exc

        if not self._policy.can_delete(
            actor=actor,
            family_member=member,
        ):
            raise PermissionError(
                "User does not have permission to delete this family member.",
            )

        snapshot = {
            "family_member_id": member.id,
            "patient_id": member.patient_id,
            "organization_id": member.organization_id,
            "family_member_number": member.family_member_number,
            "relationship": member.relationship,
            "is_next_of_kin": member.is_next_of_kin,
            "is_emergency_contact": member.is_emergency_contact,
        }

        FamilyMemberService.delete(
            instance=member,
            performed_by=actor,
        )

        event = FamilyMemberDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            **{
                **snapshot,
                "was_next_of_kin": snapshot["is_next_of_kin"],
                "was_emergency_contact": snapshot["is_emergency_contact"],
            },
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=FamilyMemberDeletionData(
                family_member_id=member.id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Patient family member deleted successfully.",
            code="family_member_deleted",
        )


__all__ = (
    "FamilyMemberDeletionData",
    "FamilyMemberDeletionRequest",
    "FamilyMemberDeletionWorkflow",
)

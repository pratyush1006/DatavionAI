"""
Patient Family Member update workflow.

Canonical mutation flow:
API → Workflow → Policy → Service → Domain Event
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.family_members.events import FamilyMemberUpdatedEvent
from apps.patient_management.family_members.models import FamilyMember
from apps.patient_management.family_members.policies import FamilyMemberPolicy
from apps.patient_management.family_members.services import FamilyMemberService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberUpdateRequest:
    family_member_id: UUID
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberUpdateData:
    family_member_id: UUID
    updated: bool
    event_id: UUID | None = None


class FamilyMemberUpdateWorkflow(
    BaseWorkflow[FamilyMemberUpdateData],
):
    """Update a tenant-scoped patient family member."""

    workflow_name = "family_member.update"

    def __init__(
        self,
        *,
        request: FamilyMemberUpdateRequest,
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
    ) -> WorkflowResult[FamilyMemberUpdateData]:
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

        if not self._policy.can_update(
            actor=actor,
            family_member=member,
        ):
            raise PermissionError(
                "User does not have permission to update this family member.",
            )

        data = dict(self._request.data)
        if not data:
            return WorkflowResult.ok(
                context=context,
                data=FamilyMemberUpdateData(
                    family_member_id=member.id,
                    updated=False,
                ),
                message="No family member changes were supplied.",
                code="family_member_unchanged",
            )

        before = {
            field: self._serialize_value(getattr(member, field))
            for field in data
            if hasattr(member, field)
        }

        updated = FamilyMemberService.update(
            instance=member,
            validated_data=data,
            performed_by=actor,
        )

        changes = {
            field: {
                "old": old,
                "new": self._serialize_value(getattr(updated, field)),
            }
            for field, old in before.items()
            if old != self._serialize_value(getattr(updated, field))
        }

        if not changes:
            return WorkflowResult.ok(
                context=context,
                data=FamilyMemberUpdateData(
                    family_member_id=updated.id,
                    updated=False,
                ),
                message="No family member changes were detected.",
                code="family_member_unchanged",
            )

        event = FamilyMemberUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            family_member_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            family_member_number=updated.family_member_number,
            relationship=updated.relationship,
            status=updated.status,
            is_next_of_kin=updated.is_next_of_kin,
            is_emergency_contact=updated.is_emergency_contact,
            changes=changes,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=FamilyMemberUpdateData(
                family_member_id=updated.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient family member updated successfully.",
            code="family_member_updated",
        )

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        if isinstance(value, UUID):
            return str(value)
        if hasattr(value, "isoformat"):
            try:
                return value.isoformat()
            except (AttributeError, TypeError, ValueError):
                pass
        return value


__all__ = (
    "FamilyMemberUpdateData",
    "FamilyMemberUpdateRequest",
    "FamilyMemberUpdateWorkflow",
)

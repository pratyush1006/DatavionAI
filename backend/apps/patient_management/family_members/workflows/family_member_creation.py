"""
Patient Family Member creation workflow.

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
from apps.patient_management.family_members.events import FamilyMemberCreatedEvent
from apps.patient_management.family_members.policies import FamilyMemberPolicy
from apps.patient_management.family_members.services import FamilyMemberService
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberCreationRequest:
    organization_id: UUID
    patient_id: UUID
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class FamilyMemberCreationData:
    family_member_id: UUID
    created: bool
    event_id: UUID | None = None


class FamilyMemberCreationWorkflow(
    BaseWorkflow[FamilyMemberCreationData],
):
    """Create a family member within the current tenant."""

    workflow_name = "family_member.create"

    def __init__(
        self,
        *,
        request: FamilyMemberCreationRequest,
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
    ) -> WorkflowResult[FamilyMemberCreationData]:
        try:
            actor = User.objects.get(pk=context.actor_id)
            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            patient = Patient.objects.get(
                pk=self._request.patient_id,
                organization_id=organization.id,
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
                "User does not have permission to create a family member.",
            )

        family_member = FamilyMemberService.create(
            validated_data={
                **self._request.data,
                "organization": organization,
                "patient": patient,
            },
            performed_by=actor,
        )

        event = FamilyMemberCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            family_member_id=family_member.id,
            patient_id=family_member.patient_id,
            organization_id=family_member.organization_id,
            family_member_number=family_member.family_member_number,
            relationship=family_member.relationship,
            status=family_member.status,
            is_next_of_kin=family_member.is_next_of_kin,
            is_emergency_contact=family_member.is_emergency_contact,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=FamilyMemberCreationData(
                family_member_id=family_member.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient family member created successfully.",
            code="family_member_created",
        )


__all__ = (
    "FamilyMemberCreationData",
    "FamilyMemberCreationRequest",
    "FamilyMemberCreationWorkflow",
)

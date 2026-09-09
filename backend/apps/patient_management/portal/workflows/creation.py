"""
Patient Portal creation workflow
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
from apps.patient_management.patients.models import Patient
from apps.patient_management.portal.events import PatientPortalAccountCreatedEvent
from apps.patient_management.portal.policies import PatientPortalPolicy
from apps.patient_management.portal.services import PatientPortalAccountService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPortalCreationRequest:
    """Input required to create a portal account."""

    organization_id: UUID
    patient_id: UUID
    data: dict


class PatientPortalCreationWorkflow(
    BaseWorkflow,
):
    """Orchestrate Patient Portal account creation."""

    workflow_name = "patient_portal.create"

    def __init__(
        self,
        *,
        request: PatientPortalCreationRequest,
        policy: PatientPortalPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the creation workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientPortalPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """Create the account and publish its domain event."""

        try:
            actor = User.objects.get(pk=context.actor_id)
            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            patient = Patient.objects.select_related(
                "organization",
            ).get(
                pk=self._request.patient_id,
                organization_id=organization.pk,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Organization, patient, or actor was not found.",
            ) from exc

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "You do not have permission to create portal accounts.",
            )

        account = PatientPortalAccountService.create(
            organization=organization,
            patient=patient,
            performed_by=actor,
            **self._request.data,
        )

        event = PatientPortalAccountCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            account_id=account.pk,
            patient_id=account.patient_id,
            organization_id=account.organization_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=account,
            message="Patient portal account created successfully.",
            code="patient_portal_created",
        )


__all__ = (
    "PatientPortalCreationRequest",
    "PatientPortalCreationWorkflow",
)

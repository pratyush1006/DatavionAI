"""
Patient creation workflow.

Coordinates the complete Patient creation lifecycle.

Responsibilities
----------------
- Resolve actor.
- Resolve tenant-scoped organization.
- Validate RBAC policy.
- Execute Patient domain service.
- Publish PatientCreatedEvent after commit.

Non-responsibilities
--------------------
- API serialization.
- Direct persistence.
- RBAC implementation.
- Domain validation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.patients.constants import (
    BloodGroup,
    PatientGender,
    PatientMaritalStatus,
)
from apps.patient_management.patients.events import (
    PatientCreatedEvent,
)
from apps.patient_management.patients.policies import (
    PatientPolicy,
)
from apps.patient_management.patients.services import (
    PatientService,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientCreationRequest:
    """
    Patient creation request.
    """

    organization_id: UUID
    first_name: str
    last_name: str
    mrn: str | None = None
    middle_name: str | None = None
    preferred_name: str | None = None
    date_of_birth: date | None = None
    gender: PatientGender | str = PatientGender.UNKNOWN
    marital_status: PatientMaritalStatus | str = PatientMaritalStatus.UNKNOWN
    blood_group: BloodGroup | str = BloodGroup.UNKNOWN
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = "India"
    postal_code: str | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientCreationData:
    """
    Patient creation result.
    """

    patient_id: UUID
    created: bool
    event_id: UUID | None = None


class PatientCreationWorkflow(
    BaseWorkflow[PatientCreationData],
):
    """
    Create a Patient inside the current tenant.
    """

    def __init__(
        self,
        *,
        request: PatientCreationRequest,
        policy: PatientPolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:
        super().__init__(
            logger_=logger_,
        )

        self._request = request
        self._policy = policy or PatientPolicy()

    @staticmethod
    def _failure(
        *,
        context: WorkflowContext,
        message: str,
        code: str,
        metadata: dict[str, Any] | None = None,
    ) -> WorkflowResult[PatientCreationData]:
        return WorkflowResult.fail(
            context=context,
            message=message,
            code=code,
            metadata=metadata or {},
        )

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientCreationData]:
        from apps.platform.accounts.models import User
        from apps.platform.organizations.models import Organization

        try:
            actor = User.objects.get(
                id=context.actor_id,
            )
        except ObjectDoesNotExist:
            return self._failure(
                context=context,
                message="Workflow actor could not be resolved.",
                code="patient_actor_not_found",
                metadata={
                    "actor_id": str(context.actor_id),
                },
            )

        try:
            organization = Organization.objects.get(
                id=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist:
            return self._failure(
                context=context,
                message=("Organization does not exist within the current tenant."),
                code="patient_organization_not_found",
                metadata={
                    "organization_id": str(
                        self._request.organization_id,
                    ),
                    "tenant_id": str(context.tenant_id),
                },
            )

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            return self._failure(
                context=context,
                message=("User does not have permission to create patient."),
                code="patient_create_forbidden",
                metadata={
                    "organization_id": str(organization.id),
                    "actor_id": str(context.actor_id),
                },
            )

        patient = PatientService.create(
            validated_data={
                "organization": organization,
                "mrn": self._request.mrn or "",
                "first_name": self._request.first_name,
                "middle_name": self._request.middle_name,
                "last_name": self._request.last_name,
                "preferred_name": self._request.preferred_name,
                "date_of_birth": self._request.date_of_birth,
                "gender": self._request.gender,
                "marital_status": self._request.marital_status,
                "blood_group": self._request.blood_group,
                "phone": self._request.phone,
                "email": self._request.email,
                "address": self._request.address,
                "city": self._request.city,
                "state": self._request.state,
                "country": self._request.country,
                "postal_code": self._request.postal_code,
            },
            performed_by=actor,
        )

        event = PatientCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            patient_id=patient.id,
            organization_id=organization.id,
        )

        self.publish_after_commit(event)

        logger.info(
            "Patient created.",
            extra={
                "workflow": "patient.create",
                "patient_id": str(patient.id),
                "organization_id": str(organization.id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
                "mrn": patient.mrn,
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientCreationData(
                patient_id=patient.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient created successfully.",
            code="patient_created",
        )


__all__: tuple[str, ...] = (
    "PatientCreationData",
    "PatientCreationRequest",
    "PatientCreationWorkflow",
)

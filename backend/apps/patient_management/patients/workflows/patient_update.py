"""
Patient update workflow.

Coordinates mutable Patient aggregate updates.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.patients.events import (
    PatientUpdatedEvent,
)
from apps.patient_management.patients.models import (
    Patient,
)
from apps.patient_management.patients.policies import (
    PatientPolicy,
)
from apps.patient_management.patients.services import (
    PatientService,
)

logger = logging.getLogger(__name__)

type PatientUpdateDataMap = Mapping[str, object]

_ALLOWED_UPDATE_FIELDS = frozenset(
    {
        "first_name",
        "middle_name",
        "last_name",
        "preferred_name",
        "date_of_birth",
        "gender",
        "marital_status",
        "blood_group",
        "phone",
        "email",
        "address",
        "city",
        "state",
        "country",
        "postal_code",
    }
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientUpdateRequest:
    """
    Patient update request.
    """

    patient_id: UUID
    data: PatientUpdateDataMap


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientUpdateData:
    """
    Patient update result.
    """

    patient_id: UUID
    updated: bool
    event_id: UUID | None = None


class PatientUpdateWorkflow(
    BaseWorkflow[PatientUpdateData],
):
    """
    Update mutable Patient information.

    Identity and lifecycle fields are intentionally protected.
    """

    def __init__(
        self,
        *,
        request: PatientUpdateRequest,
        policy: PatientPolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:
        super().__init__(
            logger_=logger_,
        )

        self._request = request
        self._policy = policy or PatientPolicy()

    def _validate_update_fields(self) -> None:
        invalid_fields = frozenset(
            self._request.data,
        ).difference(
            _ALLOWED_UPDATE_FIELDS,
        )

        if invalid_fields:
            fields = ", ".join(
                sorted(invalid_fields),
            )

            raise ValidationError(
                f"Patient update contains unsupported fields: {fields}.",
            )

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientUpdateData]:
        self._validate_update_fields()

        if not self._request.data:
            return WorkflowResult.ok(
                context=context,
                data=PatientUpdateData(
                    patient_id=self._request.patient_id,
                    updated=False,
                ),
                message="No patient changes were requested.",
                code="patient_update_no_changes",
            )

        from apps.platform.accounts.models import User

        with transaction.atomic():
            actor = User.objects.get(
                id=context.actor_id,
            )

            patient = Patient.objects.select_related("organization").get(
                id=self._request.patient_id,
                organization__tenant_id=context.tenant_id,
            )

            if not self._policy.can_manage(
                actor=actor,
                patient=patient,
            ):
                raise PermissionError(
                    "User does not have permission to update patient.",
                )

            patient = PatientService.update(
                instance=patient,
                validated_data=self._request.data,
                actor=actor,
            )

            event = PatientUpdatedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                patient_id=patient.id,
                organization_id=patient.organization_id,
            )

            self.publish_after_commit(event)

        logger.info(
            "Patient updated.",
            extra={
                "workflow": "patient.update",
                "patient_id": str(patient.id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
                "event_id": str(event.event_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientUpdateData(
                patient_id=patient.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient updated successfully.",
            code="patient_updated",
        )


__all__: tuple[str, ...] = (
    "PatientUpdateData",
    "PatientUpdateRequest",
    "PatientUpdateWorkflow",
)

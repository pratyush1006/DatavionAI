"""Bridge clinical encounter lifecycle events into Revenue Cycle work queues."""

from __future__ import annotations

from datetime import date
from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from apps.clinical.encounters.events import (
    EncounterCreated,
    EncounterStatusChanged,
)
from apps.clinical.encounters.models import Encounter
from apps.core.events import registry
from apps.insurance.constants import CoverageStatus
from apps.insurance.models import Enrollment
from apps.revenue_cycle.coding.constants import CodingType
from apps.revenue_cycle.coding.services import CodingService
from apps.revenue_cycle.insurance_verification.constants import (
    VerificationMethod,
)
from apps.revenue_cycle.insurance_verification.services import (
    InsuranceVerificationService,
)


class EncounterInsuranceHandler:
    """Create idempotent, pending verification tasks for active enrollments."""

    def handle(self, event: EncounterCreated) -> None:
        encounter = Encounter.objects.select_related(
            "organization",
            "patient",
            "appointment",
        ).get(
            pk=event.encounter_id,
            organization_id=event.organization_id,
            organization__tenant_id=event.tenant_id,
        )
        service_date = self._service_date(encounter)
        enrollments = (
            Enrollment.objects.filter(
                organization_id=encounter.organization_id,
                patient_id=encounter.patient_id,
                status=CoverageStatus.ACTIVE,
                effective_date__lte=service_date,
                plan__is_active=True,
                plan__payer__active=True,
            )
            .filter(
                Q(expiration_date__isnull=True) | Q(expiration_date__gte=service_date)
            )
            .select_related("plan__payer", "subscriber")
            .order_by("-is_primary", "effective_date", "created_at")
        )

        for enrollment in enrollments:
            payer = enrollment.plan.payer
            subscriber = enrollment.subscriber
            encounter_reference = f"encounter:{encounter.pk}:enrollment:{enrollment.pk}"
            InsuranceVerificationService.create(
                organization_id=encounter.organization_id,
                patient_id=encounter.patient_id,
                request_reference=encounter_reference,
                idempotency_key=f"{encounter_reference}:verification",
                payer_id=str(payer.pk),
                member_id=enrollment.member_id,
                data={
                    "payer_name": payer.display_name,
                    "policy_number": enrollment.policy_number,
                    "group_number": enrollment.group_number,
                    "subscriber_name": self._subscriber_name(subscriber),
                    "subscriber_relationship": enrollment.relationship_to_subscriber,
                    "verification_method": VerificationMethod.MANUAL.value,
                    "response_message": (
                        "Coverage record found. External payer eligibility "
                        "verification is still required."
                    ),
                    "response_payload": {
                        "source": "encounter_created",
                        "encounter_id": str(encounter.pk),
                        "enrollment_id": str(enrollment.pk),
                        "primary": enrollment.is_primary,
                        "enrollment_status": enrollment.status,
                    },
                },
            )

    @staticmethod
    def _service_date(encounter: Encounter) -> date:
        started_at = encounter.started_at
        if started_at is not None:
            return timezone.localtime(started_at).date()
        scheduled_start = encounter.appointment.scheduled_start
        if scheduled_start is not None:
            return timezone.localtime(scheduled_start).date()
        return timezone.localdate()

    @staticmethod
    def _subscriber_name(subscriber: Any | None) -> str:
        if subscriber is None:
            return ""
        name = " ".join(
            part
            for part in (
                getattr(subscriber, "first_name", ""),
                getattr(subscriber, "last_name", ""),
            )
            if part
        ).strip()
        return name or str(getattr(subscriber, "subscriber_identifier", ""))


class EncounterCodingHandler:
    """Queue a coding work item after the clinical encounter is completed."""

    def handle(self, event: EncounterStatusChanged) -> None:
        if event.new_status != "completed":
            return

        encounter = Encounter.objects.select_related(
            "organization",
            "patient",
            "appointment",
        ).get(
            pk=event.encounter_id,
            organization_id=event.organization_id,
            organization__tenant_id=event.tenant_id,
        )
        actor = get_user_model().objects.filter(pk=event.actor_id).first()

        summary_parts = [
            encounter.chief_complaint,
            encounter.history_of_present_illness,
            encounter.assessment,
            encounter.plan,
        ]
        clinical_summary = "\n\n".join(
            part.strip() for part in summary_parts if part and part.strip()
        )

        service_date = self._service_date(encounter)
        CodingService.create(
            organization=encounter.organization,
            tenant_id=event.tenant_id,
            patient=encounter.patient,
            actor=actor,
            idempotency_key=f"encounter:{encounter.pk}:coding",
            source_reference=str(encounter.pk),
            service_date=service_date,
            coding_type=CodingType.PROFESSIONAL.value,
            encounter_type=str(encounter.appointment.appointment_type),
            clinical_summary=clinical_summary,
            documentation={
                "encounter_id": str(encounter.pk),
                "encounter_number": encounter.encounter_number,
                "appointment_id": str(encounter.appointment_id),
            },
            coding_notes=(
                "Created from completed encounter; clinical and billing codes "
                "require coder review before claim preparation."
            ),
        )

    @staticmethod
    def _service_date(encounter: Encounter) -> date:
        timestamp = encounter.ended_at or encounter.started_at
        if timestamp is not None:
            return timezone.localtime(timestamp).date()
        return timezone.localdate()


def register_encounter_handlers() -> None:
    """Register the clinical-to-revenue-cycle event handlers once per process."""

    registry.register(EncounterCreated, EncounterInsuranceHandler())
    registry.register(EncounterStatusChanged, EncounterCodingHandler())


__all__ = (
    "EncounterCodingHandler",
    "EncounterInsuranceHandler",
    "register_encounter_handlers",
)

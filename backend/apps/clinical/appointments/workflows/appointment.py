"""Workflow orchestration for Clinical Appointments."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.clinical.appointments.constants import AppointmentStatus
from apps.clinical.appointments.events import (
    AppointmentCreated,
    AppointmentDeleted,
    AppointmentStatusChanged,
    AppointmentUpdated,
)
from apps.clinical.appointments.policies import AppointmentPolicy
from apps.clinical.appointments.selectors import AppointmentSelector
from apps.clinical.appointments.services import AppointmentService
from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AppointmentBookingRequest:
    """Input contract for Appointment creation."""

    organization_id: UUID
    patient_id: UUID
    provider_id: UUID
    scheduled_start: object
    scheduled_end: object
    data: dict
    actor: object
    idempotency_key: str = ""


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AppointmentUpdateRequest:
    """Input contract for Appointment updates."""

    organization_id: UUID
    appointment_id: UUID
    data: dict
    actor: object


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AppointmentDeleteRequest:
    """Input contract for Appointment deletion."""

    organization_id: UUID
    appointment_id: UUID
    actor: object


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AppointmentRescheduleRequest:
    """Input contract for Appointment rescheduling."""

    organization_id: UUID
    appointment_id: UUID
    scheduled_start: object
    scheduled_end: object
    duration_minutes: int
    actor: object


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AppointmentCancelRequest:
    """Input contract for Appointment cancellation."""

    organization_id: UUID
    appointment_id: UUID
    reason: str
    actor: object


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AppointmentLifecycleRequest:
    """Input contract for a lifecycle status transition."""

    organization_id: UUID
    appointment_id: UUID
    target_status: str
    actor: object
    reason: str = ""


def _resolve_actor(
    context: WorkflowContext,
    fallback_actor,
):
    """Resolve the authenticated workflow actor."""

    return User.objects.get(
        pk=context.actor_id or fallback_actor.pk,
    )


def _resolve_organization(
    context: WorkflowContext,
    organization_id,
):
    """Resolve an organization inside the active tenant boundary."""

    return Organization.objects.get(
        pk=organization_id,
        tenant_id=context.tenant_id,
    )


class AppointmentBookingWorkflow(BaseWorkflow):
    """Create an appointment through the application workflow."""

    workflow_name = "appointment.create"

    def __init__(
        self,
        *,
        request: AppointmentBookingRequest,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize the booking workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or AppointmentPolicy()

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """Create an appointment and publish its event."""

        actor = _resolve_actor(
            context,
            self._request.actor,
        )
        organization = _resolve_organization(
            context,
            self._request.organization_id,
        )

        patient = Patient.objects.get(
            pk=self._request.patient_id,
            organization_id=organization.pk,
        )

        from apps.clinical.providers.models import Provider

        provider = Provider.objects.get(
            pk=self._request.provider_id,
            organization_id=organization.pk,
        )

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to create appointments.",
            )

        record = AppointmentService.create(
            organization=organization,
            patient=patient,
            provider=provider,
            scheduled_start=self._request.scheduled_start,
            scheduled_end=self._request.scheduled_end,
            data=self._request.data,
            actor=actor,
            idempotency_key=self._request.idempotency_key,
        )

        event = AppointmentCreated(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            appointment_id=record.id,
            organization_id=record.organization_id,
            patient_id=record.patient_id,
            provider_id=record.provider_id,
            status=record.status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="Appointment created successfully.",
            code="appointment_created",
        )


class AppointmentUpdateWorkflow(BaseWorkflow):
    """Update an appointment through the application workflow."""

    workflow_name = "appointment.update"

    def __init__(
        self,
        *,
        request: AppointmentUpdateRequest,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize the update workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or AppointmentPolicy()

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """Update an appointment and publish its event."""

        actor = _resolve_actor(
            context,
            self._request.actor,
        )
        organization = _resolve_organization(
            context,
            self._request.organization_id,
        )
        record = AppointmentSelector.get(
            organization=organization,
            appointment_id=self._request.appointment_id,
        )

        if not self._policy.can_update(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to update appointments.",
            )

        record = AppointmentService.update(
            record=record,
            data=self._request.data,
        )

        event = AppointmentUpdated(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            appointment_id=record.id,
            organization_id=record.organization_id,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="Appointment updated successfully.",
            code="appointment_updated",
        )


class AppointmentDeleteWorkflow(BaseWorkflow):
    """Delete an appointment through the application workflow."""

    workflow_name = "appointment.delete"

    def __init__(
        self,
        *,
        request: AppointmentDeleteRequest,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize the deletion workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or AppointmentPolicy()

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """Soft-delete an appointment and publish its event."""

        actor = _resolve_actor(
            context,
            self._request.actor,
        )
        organization = _resolve_organization(
            context,
            self._request.organization_id,
        )
        record = AppointmentSelector.get(
            organization=organization,
            appointment_id=self._request.appointment_id,
        )

        if not self._policy.can_delete(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to delete appointments.",
            )

        record = AppointmentService.delete(
            record=record,
            actor=actor,
        )

        event = AppointmentDeleted(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            appointment_id=record.id,
            organization_id=record.organization_id,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="Appointment deleted successfully.",
            code="appointment_deleted",
        )


class AppointmentTransitionWorkflow(BaseWorkflow):
    """Apply an Appointment lifecycle transition."""

    workflow_name = "appointment.transition"

    def __init__(
        self,
        *,
        request: AppointmentLifecycleRequest,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize the lifecycle workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or AppointmentPolicy()

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """Apply a lifecycle transition and publish its event."""

        actor = _resolve_actor(
            context,
            self._request.actor,
        )
        organization = _resolve_organization(
            context,
            self._request.organization_id,
        )
        record = AppointmentSelector.get(
            organization=organization,
            appointment_id=self._request.appointment_id,
        )

        if not self._policy.can_transition(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to transition appointments.",
            )

        previous = record.status

        record = AppointmentService.transition(
            record=record,
            target_status=self._request.target_status,
            reason=self._request.reason,
            actor=actor,
        )

        event = AppointmentStatusChanged(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            appointment_id=record.id,
            organization_id=record.organization_id,
            previous_status=previous,
            status=record.status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="Appointment status updated successfully.",
            code="appointment_status_changed",
        )


class AppointmentConfirmWorkflow(AppointmentTransitionWorkflow):
    """Confirm an appointment."""

    workflow_name = "appointment.confirm"

    def __init__(
        self,
        *,
        organization_id,
        appointment_id,
        actor,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize confirmation."""

        super().__init__(
            request=AppointmentLifecycleRequest(
                organization_id=organization_id,
                appointment_id=appointment_id,
                target_status=AppointmentStatus.CONFIRMED,
                actor=actor,
            ),
            policy=policy,
            logger_=logger_,
        )


class AppointmentCheckInWorkflow(AppointmentTransitionWorkflow):
    """Check in an appointment."""

    workflow_name = "appointment.check_in"

    def __init__(
        self,
        *,
        organization_id,
        appointment_id,
        actor,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize check-in."""

        super().__init__(
            request=AppointmentLifecycleRequest(
                organization_id=organization_id,
                appointment_id=appointment_id,
                target_status=AppointmentStatus.CHECKED_IN,
                actor=actor,
            ),
            policy=policy,
            logger_=logger_,
        )


class AppointmentStartWorkflow(AppointmentTransitionWorkflow):
    """Start an appointment."""

    workflow_name = "appointment.start"

    def __init__(
        self,
        *,
        organization_id,
        appointment_id,
        actor,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize start."""

        super().__init__(
            request=AppointmentLifecycleRequest(
                organization_id=organization_id,
                appointment_id=appointment_id,
                target_status=AppointmentStatus.IN_PROGRESS,
                actor=actor,
            ),
            policy=policy,
            logger_=logger_,
        )


class AppointmentCompleteWorkflow(AppointmentTransitionWorkflow):
    """Complete an appointment."""

    workflow_name = "appointment.complete"

    def __init__(
        self,
        *,
        organization_id,
        appointment_id,
        actor,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize completion."""

        super().__init__(
            request=AppointmentLifecycleRequest(
                organization_id=organization_id,
                appointment_id=appointment_id,
                target_status=AppointmentStatus.COMPLETED,
                actor=actor,
            ),
            policy=policy,
            logger_=logger_,
        )


class AppointmentNoShowWorkflow(AppointmentTransitionWorkflow):
    """Mark a missed appointment without refunding the booking deposit."""

    workflow_name = "appointment.no_show"

    def __init__(
        self, *, organization_id, appointment_id, actor, policy=None, logger_=None
    ) -> None:
        super().__init__(
            request=AppointmentLifecycleRequest(
                organization_id=organization_id,
                appointment_id=appointment_id,
                target_status=AppointmentStatus.NO_SHOW,
                actor=actor,
            ),
            policy=policy,
            logger_=logger_,
        )


class AppointmentCancelWorkflow(AppointmentTransitionWorkflow):
    """Cancel an appointment."""

    workflow_name = "appointment.cancel"

    def __init__(
        self,
        *,
        request: AppointmentCancelRequest,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize cancellation."""

        super().__init__(
            request=AppointmentLifecycleRequest(
                organization_id=request.organization_id,
                appointment_id=request.appointment_id,
                target_status=AppointmentStatus.CANCELLED,
                actor=request.actor,
                reason=request.reason,
            ),
            policy=policy,
            logger_=logger_,
        )


class AppointmentRescheduleWorkflow(BaseWorkflow):
    """Reschedule an appointment."""

    workflow_name = "appointment.reschedule"

    def __init__(
        self,
        *,
        request: AppointmentRescheduleRequest,
        policy=None,
        logger_=None,
    ) -> None:
        """Initialize rescheduling."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or AppointmentPolicy()

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """Reschedule an appointment."""

        actor = _resolve_actor(
            context,
            self._request.actor,
        )
        organization = _resolve_organization(
            context,
            self._request.organization_id,
        )
        record = AppointmentSelector.get(
            organization=organization,
            appointment_id=self._request.appointment_id,
        )

        if not self._policy.can_transition(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to reschedule appointments.",
            )

        previous = record.status

        record = AppointmentService.reschedule(
            record=record,
            scheduled_start=self._request.scheduled_start,
            scheduled_end=self._request.scheduled_end,
            duration_minutes=self._request.duration_minutes,
        )

        event = AppointmentStatusChanged(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            appointment_id=record.id,
            organization_id=record.organization_id,
            previous_status=previous,
            status=record.status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="Appointment rescheduled successfully.",
            code="appointment_rescheduled",
        )


__all__ = (
    "AppointmentBookingRequest",
    "AppointmentBookingWorkflow",
    "AppointmentCancelRequest",
    "AppointmentCancelWorkflow",
    "AppointmentCheckInWorkflow",
    "AppointmentCompleteWorkflow",
    "AppointmentConfirmWorkflow",
    "AppointmentDeleteRequest",
    "AppointmentDeleteWorkflow",
    "AppointmentLifecycleRequest",
    "AppointmentRescheduleRequest",
    "AppointmentRescheduleWorkflow",
    "AppointmentStartWorkflow",
    "AppointmentTransitionWorkflow",
    "AppointmentUpdateRequest",
    "AppointmentUpdateWorkflow",
)

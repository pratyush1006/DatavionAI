"""Patient guarantor workflows."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast
from uuid import UUID

from apps.revenue_cycle.billing.patient_billing.events import (
    PatientBillingDomainEvent,
    publish_after_commit,
)
from apps.revenue_cycle.billing.patient_billing.policies import PatientBillingPolicy
from apps.revenue_cycle.billing.patient_billing.services import PatientGuarantorService


class PatientGuarantorWorkflow:
    """Orchestrate guarantor authorization, mutation, and events."""

    @staticmethod
    def create(
        *,
        actor: Any,
        organization: Any,
        patient: Any,
        validated_data: Mapping[str, Any],
    ) -> Any:
        """Create a guarantor."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.GUARANTOR_CREATE,
            organization=organization,
        )
        guarantor = PatientGuarantorService.create(
            organization=organization,
            patient=patient,
            validated_data=validated_data,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=guarantor.id,
                organization_id=cast(Any, guarantor).organization_id,
                patient_id=cast(Any, guarantor).patient_id,
                action="created",
            ),
        )
        return guarantor

    @staticmethod
    def update(
        *,
        actor: Any,
        organization: Any,
        instance: Any,
        validated_data: Mapping[str, Any],
    ) -> Any:
        """Update a guarantor."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.GUARANTOR_UPDATE,
            organization=organization,
        )
        guarantor = PatientGuarantorService.update(
            organization_id=organization.id,
            instance=instance,
            validated_data=validated_data,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=guarantor.id,
                organization_id=cast(Any, guarantor).organization_id,
                patient_id=cast(Any, guarantor).patient_id,
                action="updated",
            ),
        )
        return guarantor

    @staticmethod
    def delete(
        *,
        actor: Any,
        organization: Any,
        instance: Any,
    ) -> Any:
        """Soft-delete a guarantor."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.GUARANTOR_DELETE,
            organization=organization,
        )
        guarantor = PatientGuarantorService.delete(
            organization_id=organization.id,
            instance=instance,
            user_id=actor.id,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=guarantor.id,
                organization_id=cast(Any, guarantor).organization_id,
                patient_id=cast(Any, guarantor).patient_id,
                action="deleted",
            ),
        )
        return guarantor

    @staticmethod
    def restore(
        *,
        actor: Any,
        organization: Any,
        guarantor_id: UUID,
    ) -> Any:
        """Restore a guarantor."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.GUARANTOR_RESTORE,
            organization=organization,
        )
        guarantor = PatientGuarantorService.restore(
            organization_id=organization.id,
            guarantor_id=guarantor_id,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=guarantor.id,
                organization_id=cast(Any, guarantor).organization_id,
                patient_id=cast(Any, guarantor).patient_id,
                action="restored",
            ),
        )
        return guarantor


__all__ = ("PatientGuarantorWorkflow",)

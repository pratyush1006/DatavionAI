"""Patient responsibility workflows."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import UUID

from apps.billing.patient_billing.events import (
    PatientBillingDomainEvent,
    publish_after_commit,
)
from apps.billing.patient_billing.policies import PatientBillingPolicy
from apps.billing.patient_billing.services import PatientResponsibilityService


class PatientResponsibilityWorkflow:
    """Orchestrate responsibility authorization, mutation, and events."""

    @staticmethod
    def create(
        *,
        actor: Any,
        organization: Any,
        account: Any,
        validated_data: Mapping[str, Any],
    ) -> Any:
        """Create a responsibility record."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.RESPONSIBILITY_CREATE,
            organization=organization,
        )
        responsibility = PatientResponsibilityService.create(
            organization_id=organization.id,
            account_id=account.id,
            validated_data=validated_data,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=responsibility.id,
                organization_id=organization.id,
                patient_id=account.patient_id,
                action="created",
            ),
        )
        return responsibility

    @staticmethod
    def update(
        *,
        actor: Any,
        organization: Any,
        instance: Any,
        validated_data: Mapping[str, Any],
    ) -> Any:
        """Update a responsibility record."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.RESPONSIBILITY_UPDATE,
            organization=organization,
        )
        responsibility = PatientResponsibilityService.update(
            organization_id=organization.id,
            instance=instance,
            validated_data=validated_data,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=responsibility.id,
                organization_id=organization.id,
                patient_id=responsibility.account.patient_id,
                action="updated",
            ),
        )
        return responsibility

    @staticmethod
    def delete(
        *,
        actor: Any,
        organization: Any,
        instance: Any,
    ) -> Any:
        """Soft-delete a responsibility record."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.RESPONSIBILITY_DELETE,
            organization=organization,
        )
        responsibility = PatientResponsibilityService.delete(
            organization_id=organization.id,
            instance=instance,
            user_id=actor.id,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=responsibility.id,
                organization_id=organization.id,
                patient_id=responsibility.account.patient_id,
                action="deleted",
            ),
        )
        return responsibility

    @staticmethod
    def restore(
        *,
        actor: Any,
        organization: Any,
        responsibility_id: UUID,
    ) -> Any:
        """Restore a responsibility record."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.RESPONSIBILITY_RESTORE,
            organization=organization,
        )
        responsibility = PatientResponsibilityService.restore(
            organization_id=organization.id,
            responsibility_id=responsibility_id,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=responsibility.id,
                organization_id=organization.id,
                patient_id=responsibility.account.patient_id,
                action="restored",
            ),
        )
        return responsibility


__all__ = ("PatientResponsibilityWorkflow",)

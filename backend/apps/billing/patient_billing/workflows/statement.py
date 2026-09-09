"""Patient statement workflows."""

from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from apps.billing.patient_billing.events import (
    PatientBillingDomainEvent,
    publish_after_commit,
)
from apps.billing.patient_billing.policies import PatientBillingPolicy
from apps.billing.patient_billing.services import PatientBillingStatementService


class PatientBillingStatementWorkflow:
    """Orchestrate statement authorization, mutation, and events."""

    @staticmethod
    def generate(
        *,
        actor: Any,
        organization: Any,
        account_id: UUID,
        period_start: date,
        period_end: date,
    ) -> Any:
        """Generate a patient statement."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.STATEMENT_CREATE,
            organization=organization,
        )
        statement = PatientBillingStatementService.generate(
            organization_id=organization.id,
            account_id=account_id,
            period_start=period_start,
            period_end=period_end,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=statement.id,
                organization_id=organization.id,
                patient_id=statement.account.patient_id,
                action="generated",
            ),
        )
        return statement

    @staticmethod
    def issue(
        *,
        actor: Any,
        organization: Any,
        statement_id: UUID,
    ) -> Any:
        """Issue a statement."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.STATEMENT_ISSUE,
            organization=organization,
        )
        statement = PatientBillingStatementService.issue(
            organization_id=organization.id,
            statement_id=statement_id,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=statement.id,
                organization_id=organization.id,
                patient_id=statement.account.patient_id,
                action="issued",
            ),
        )
        return statement

    @staticmethod
    def void(
        *,
        actor: Any,
        organization: Any,
        statement_id: UUID,
    ) -> Any:
        """Void a statement."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.STATEMENT_VOID,
            organization=organization,
        )
        statement = PatientBillingStatementService.void(
            organization_id=organization.id,
            statement_id=statement_id,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=statement.id,
                organization_id=organization.id,
                patient_id=statement.account.patient_id,
                action="voided",
            ),
        )
        return statement


__all__ = ("PatientBillingStatementWorkflow",)

"""Patient Billing account workflows."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, cast
from uuid import UUID

from apps.revenue_cycle.billing.patient_billing.events import (
    PatientBillingDomainEvent,
    publish_after_commit,
)
from apps.revenue_cycle.billing.patient_billing.policies import PatientBillingPolicy
from apps.revenue_cycle.billing.patient_billing.services import (
    PatientBillingAccountService,
)


class PatientBillingAccountWorkflow:
    """Orchestrate account authorization, mutation, and events."""

    @staticmethod
    def create(
        *,
        actor: Any,
        organization: Any,
        patient: Any,
        account_number: str,
        currency: str = "INR",
        opening_balance: Decimal = Decimal("0.00"),
        credit_limit: Decimal = Decimal("0.00"),
        notes: str = "",
    ) -> Any:
        """Create an account through the policy and service boundaries."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.ACCOUNT_CREATE,
            organization=organization,
        )
        account = PatientBillingAccountService.create(
            organization=organization,
            patient=patient,
            account_number=account_number,
            currency=currency,
            opening_balance=opening_balance,
            credit_limit=credit_limit,
            notes=notes,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=account.id,
                organization_id=cast(Any, account).organization_id,
                patient_id=cast(Any, account).patient_id,
                action="created",
            ),
        )
        return account

    @staticmethod
    def update(
        *,
        actor: Any,
        organization: Any,
        instance: Any,
        validated_data: Mapping[str, Any],
    ) -> Any:
        """Update an account through policy and service boundaries."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.ACCOUNT_UPDATE,
            organization=organization,
        )
        account = PatientBillingAccountService.update(
            organization_id=organization.id,
            instance=instance,
            validated_data=validated_data,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=account.id,
                organization_id=cast(Any, account).organization_id,
                patient_id=cast(Any, account).patient_id,
                action="updated",
            ),
        )
        return account

    @staticmethod
    def transition(
        *,
        actor: Any,
        organization: Any,
        account_id: UUID,
        status: str,
    ) -> Any:
        """Transition an account through policy and service boundaries."""

        PatientBillingPolicy.require(
            actor=actor,
            permission=PatientBillingPolicy.ACCOUNT_LIFECYCLE,
            organization=organization,
        )
        account = PatientBillingAccountService.transition(
            organization_id=organization.id,
            account_id=account_id,
            status=status,
        )
        publish_after_commit(
            PatientBillingDomainEvent(
                tenant_id=organization.tenant_id,
                actor_id=actor.id,
                aggregate_id=account.id,
                organization_id=cast(Any, account).organization_id,
                patient_id=cast(Any, account).patient_id,
                action="lifecycle_changed",
                changes={"status": status},
            ),
        )
        return account


__all__ = ("PatientBillingAccountWorkflow",)

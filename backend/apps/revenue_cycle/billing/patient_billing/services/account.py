"""Patient billing account domain services."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.revenue_cycle.billing.patient_billing.constants import (
    PatientBillingAccountStatus,
)
from apps.revenue_cycle.billing.patient_billing.exceptions import (
    PatientBillingLifecycleError,
)
from apps.revenue_cycle.billing.patient_billing.models import PatientBillingAccount


class PatientBillingAccountService:
    """Execute transactional account mutations within an organization."""

    @staticmethod
    @transaction.atomic
    def create(
        *,
        organization: Any,
        patient: Any,
        account_number: str,
        currency: str = "INR",
        opening_balance: Decimal = Decimal("0.00"),
        credit_limit: Decimal = Decimal("0.00"),
        notes: str = "",
    ) -> PatientBillingAccount:
        """Create a patient billing account after validating ownership."""

        if patient.organization_id != organization.id:
            raise PatientBillingLifecycleError(
                "Patient does not belong to the billing organization.",
            )
        account = PatientBillingAccount(
            organization=organization,
            patient=patient,
            account_number=account_number.strip(),
            currency=currency,
            opening_balance=opening_balance,
            current_balance=opening_balance,
            credit_limit=credit_limit,
            notes=notes.strip(),
        )
        account.full_clean()
        account.save()
        return account

    @staticmethod
    @transaction.atomic
    def update(
        *,
        organization_id: UUID,
        instance: PatientBillingAccount,
        validated_data: Mapping[str, Any],
    ) -> PatientBillingAccount:
        """Update mutable account fields under an organization-scoped lock."""

        account: PatientBillingAccount = (
            PatientBillingAccount.objects.select_for_update().get(
                id=instance.id,
                organization_id=organization_id,
            )
        )
        for field in ("currency", "credit_limit", "notes"):
            if field in validated_data:
                setattr(account, field, validated_data[field])
        account.full_clean()
        account.save(
            update_fields=(
                "currency",
                "credit_limit",
                "notes",
                "updated_at",
            ),
        )
        return account

    @staticmethod
    @transaction.atomic
    def transition(
        *,
        organization_id: UUID,
        account_id: UUID,
        status: str,
    ) -> PatientBillingAccount:
        """Transition an account using a tenant-scoped row lock."""

        account: PatientBillingAccount = (
            PatientBillingAccount.objects.select_for_update().get(
                id=account_id,
                organization_id=organization_id,
            )
        )
        allowed = {
            PatientBillingAccountStatus.ACTIVE: {
                PatientBillingAccountStatus.SUSPENDED,
                PatientBillingAccountStatus.CLOSED,
            },
            PatientBillingAccountStatus.SUSPENDED: {
                PatientBillingAccountStatus.ACTIVE,
                PatientBillingAccountStatus.CLOSED,
            },
            PatientBillingAccountStatus.CLOSED: set(),
        }
        if status not in allowed.get(account.status, set()):
            raise PatientBillingLifecycleError(
                f"Cannot transition account from {account.status} to {status}.",
            )
        account.status = status
        account.save(
            update_fields=(
                "status",
                "updated_at",
            ),
        )
        return account


__all__ = ("PatientBillingAccountService",)

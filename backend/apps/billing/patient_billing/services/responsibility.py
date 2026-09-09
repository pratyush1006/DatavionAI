"""Patient financial responsibility services.

The service layer enforces organization boundaries and account-level financial
responsibility invariants under a locked Patient Billing account aggregate.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import date, timedelta
from decimal import Decimal
from typing import Any
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.billing.patient_billing.exceptions import PatientBillingOrganizationError
from apps.billing.patient_billing.models import (
    PatientBillingAccount,
    PatientFinancialResponsibility,
)


def validate_responsibility_allocation(
    records: Iterable[Any],
) -> None:
    """Validate payer allocation and overlapping-responsibility invariants."""

    materialized = tuple(records)
    for index, current in enumerate(materialized):
        current_start = current.effective_from
        current_end = current.effective_to
        for other in materialized[index + 1 :]:
            other_start = other.effective_from
            other_end = other.effective_to
            overlaps = (current_end is None or other_start <= current_end) and (
                other_end is None or current_start <= other_end
            )
            if not overlaps:
                continue
            same_party = (
                current.party_type == other.party_type
                and current.guarantor_id == other.guarantor_id
            )
            if same_party:
                raise ValidationError(
                    "Overlapping responsibility periods for the same payer are not allowed.",
                )

    events: dict[date, Decimal] = {}
    for record in materialized:
        events[record.effective_from] = (
            events.get(record.effective_from, Decimal("0.00")) + record.percentage
        )
        if record.effective_to is not None and record.effective_to < date.max:
            end_marker = record.effective_to + timedelta(days=1)
            events[end_marker] = (
                events.get(end_marker, Decimal("0.00")) - record.percentage
            )

    running_total = Decimal("0.00")
    for event_date in sorted(events):
        running_total += events[event_date]
        if running_total > Decimal("100.00"):
            raise ValidationError(
                {
                    "percentage": (
                        "Active financial responsibility allocations cannot exceed 100%."
                    ),
                }
            )


class PatientResponsibilityService:
    """Execute transactional financial responsibility mutations."""

    @staticmethod
    def _validate_guarantor_boundary(
        *,
        account: PatientBillingAccount,
        guarantor: Any,
    ) -> None:
        """Ensure a guarantor belongs to the account's Patient and organization."""

        if guarantor is not None and (
            guarantor.organization_id != account.organization_id
            or guarantor.patient_id != account.patient_id
            or guarantor.is_deleted
        ):
            raise PatientBillingOrganizationError(
                "Guarantor is outside the billing account boundary or is deleted.",
            )

    @staticmethod
    def _validate_allocation(
        *,
        account: PatientBillingAccount,
        candidate: PatientFinancialResponsibility,
        exclude_id: UUID | None = None,
    ) -> None:
        """Validate candidate allocation against all active account records."""

        queryset = PatientFinancialResponsibility.objects.filter(
            account_id=account.id,
        )
        if exclude_id is not None:
            queryset = queryset.exclude(id=exclude_id)
        validate_responsibility_allocation(
            (*queryset, candidate),
        )

    @staticmethod
    @transaction.atomic
    def create(
        *,
        organization_id: UUID,
        account_id: UUID,
        validated_data: Mapping[str, Any],
    ) -> PatientFinancialResponsibility:
        """Create responsibility after locking and validating the account aggregate."""

        account = PatientBillingAccount.objects.select_for_update().get(
            id=account_id,
            organization_id=organization_id,
        )
        guarantor = validated_data.get("guarantor")
        PatientResponsibilityService._validate_guarantor_boundary(
            account=account,
            guarantor=guarantor,
        )
        responsibility = PatientFinancialResponsibility(
            account=account,
            **validated_data,
        )
        responsibility.full_clean()
        PatientResponsibilityService._validate_allocation(
            account=account,
            candidate=responsibility,
        )
        responsibility.save()
        return responsibility

    @staticmethod
    @transaction.atomic
    def update(
        *,
        organization_id: UUID,
        instance: PatientFinancialResponsibility,
        validated_data: Mapping[str, Any],
    ) -> PatientFinancialResponsibility:
        """Update responsibility under an account-level lock and revalidation."""

        responsibility = (
            PatientFinancialResponsibility.objects.select_for_update()
            .select_related("account")
            .get(
                id=instance.id,
                account__organization_id=organization_id,
            )
        )
        account = PatientBillingAccount.objects.select_for_update().get(
            id=responsibility.account_id,
            organization_id=organization_id,
        )
        guarantor = validated_data.get(
            "guarantor",
            responsibility.guarantor,
        )
        PatientResponsibilityService._validate_guarantor_boundary(
            account=account,
            guarantor=guarantor,
        )
        for field in (
            "party_type",
            "guarantor",
            "percentage",
            "priority",
            "effective_from",
            "effective_to",
            "notes",
        ):
            if field in validated_data:
                setattr(responsibility, field, validated_data[field])
        responsibility.full_clean()
        PatientResponsibilityService._validate_allocation(
            account=account,
            candidate=responsibility,
            exclude_id=responsibility.id,
        )
        responsibility.save()
        return responsibility

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        organization_id: UUID,
        instance: PatientFinancialResponsibility,
        user_id: Any = None,
    ) -> PatientFinancialResponsibility:
        """Soft-delete responsibility inside the organization boundary."""

        responsibility = (
            PatientFinancialResponsibility.objects.select_for_update()
            .select_related("account")
            .get(
                id=instance.id,
                account__organization_id=organization_id,
            )
        )
        responsibility.delete(user_id=user_id)
        return responsibility

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        organization_id: UUID,
        responsibility_id: UUID,
    ) -> PatientFinancialResponsibility:
        """Restore responsibility after revalidating its account allocation."""

        responsibility = (
            PatientFinancialResponsibility.all_objects.select_for_update()
            .select_related("account")
            .get(
                id=responsibility_id,
                account__organization_id=organization_id,
                is_deleted=True,
            )
        )
        account = PatientBillingAccount.objects.select_for_update().get(
            id=responsibility.account_id,
            organization_id=organization_id,
        )
        PatientResponsibilityService._validate_guarantor_boundary(
            account=account,
            guarantor=responsibility.guarantor,
        )
        PatientResponsibilityService._validate_allocation(
            account=account,
            candidate=responsibility,
        )
        responsibility.restore()
        return responsibility


__all__ = (
    "PatientResponsibilityService",
    "validate_responsibility_allocation",
)

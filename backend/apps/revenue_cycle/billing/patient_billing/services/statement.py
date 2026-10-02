"""Patient billing statement services."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any, cast
from uuid import UUID, uuid4

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.revenue_cycle.billing.models.healthcare_models import (
    HealthcareInvoice as Invoice,
)
from apps.revenue_cycle.billing.models.healthcare_models import (
    HealthcarePayment as Payment,
)
from apps.revenue_cycle.billing.patient_billing.constants import PatientStatementStatus
from apps.revenue_cycle.billing.patient_billing.exceptions import (
    PatientBillingLifecycleError,
)
from apps.revenue_cycle.billing.patient_billing.models import (
    PatientBillingAccount,
    PatientBillingStatement,
)


class PatientBillingStatementService:
    """Generate and transition patient billing statements."""

    @staticmethod
    def _statement_number() -> str:
        """Return a collision-resistant statement number."""

        return f"STMT-{uuid4().hex.upper()}"

    @staticmethod
    def _eligible_invoice_statuses() -> set[str]:
        """Return invoice statuses that contribute to patient statements."""

        return {"DRAFT", "ISSUED", "PARTIALLY_PAID", "PAID", "OVERDUE"}

    @staticmethod
    @transaction.atomic
    def generate(
        *,
        organization_id: UUID,
        account_id: UUID,
        period_start: date,
        period_end: date,
    ) -> PatientBillingStatement:
        """Generate one deterministic statement for an account and period."""

        if period_end < period_start:
            raise PatientBillingLifecycleError(
                "Statement period is invalid.",
            )

        account = (
            PatientBillingAccount.objects.select_for_update()
            .select_related("patient")
            .get(
                id=account_id,
                organization_id=organization_id,
            )
        )

        existing = cast(
            PatientBillingStatement | None,
            PatientBillingStatement.objects.filter(
                account_id=account.id,
                period_start=period_start,
                period_end=period_end,
            ).first(),
        )
        if existing is not None:
            return existing

        eligible_statuses = PatientBillingStatementService._eligible_invoice_statuses()
        prior_invoices = cast(Any, Invoice.objects).filter(
            organization_id=account.organization_id,
            patient_id=account.patient_id,
            invoice_date__lt=period_start,
            status__in=eligible_statuses,
        )
        period_invoices = cast(Any, Invoice.objects).filter(
            organization_id=account.organization_id,
            patient_id=account.patient_id,
            invoice_date__gte=period_start,
            invoice_date__lte=period_end,
            status__in=eligible_statuses,
        )
        prior_payments = cast(Any, Payment.objects).filter(
            organization_id=account.organization_id,
            patient_id=account.patient_id,
            payment_date__lt=period_start,
            is_refunded=False,
        )
        period_payments = cast(Any, Payment.objects).filter(
            organization_id=account.organization_id,
            patient_id=account.patient_id,
            payment_date__gte=period_start,
            payment_date__lte=period_end,
            is_refunded=False,
        )

        prior_charges = sum(
            (invoice.total_amount for invoice in prior_invoices),
            Decimal("0.00"),
        )
        prior_paid = sum(
            (payment.amount for payment in prior_payments),
            Decimal("0.00"),
        )
        charges = sum(
            (invoice.total_amount for invoice in period_invoices),
            Decimal("0.00"),
        )
        paid = sum(
            (payment.amount for payment in period_payments),
            Decimal("0.00"),
        )
        opening = account.opening_balance + prior_charges - prior_paid
        closing = opening + charges - paid

        try:
            statement: PatientBillingStatement = PatientBillingStatement.objects.create(
                account=account,
                statement_number=PatientBillingStatementService._statement_number(),
                period_start=period_start,
                period_end=period_end,
                opening_balance=opening,
                charges=charges,
                payments=paid,
                adjustments=Decimal("0.00"),
                closing_balance=closing,
            )
            return statement
        except IntegrityError:
            return cast(
                PatientBillingStatement,
                PatientBillingStatement.objects.get(
                    account_id=account.id,
                    period_start=period_start,
                    period_end=period_end,
                ),
            )

    @staticmethod
    @transaction.atomic
    def issue(
        *,
        organization_id: UUID,
        statement_id: UUID,
    ) -> PatientBillingStatement:
        """Issue a draft statement inside the organization boundary."""

        statement: PatientBillingStatement = (
            PatientBillingStatement.objects.select_for_update().get(
                id=statement_id,
                account__organization_id=organization_id,
            )
        )
        if statement.status != PatientStatementStatus.DRAFT:
            raise PatientBillingLifecycleError(
                "Only draft statements can be issued.",
            )
        statement.status = PatientStatementStatus.ISSUED
        statement.issued_at = timezone.now()
        statement.save(
            update_fields=(
                "status",
                "issued_at",
                "updated_at",
            ),
        )
        return statement

    @staticmethod
    @transaction.atomic
    def void(
        *,
        organization_id: UUID,
        statement_id: UUID,
    ) -> PatientBillingStatement:
        """Void a draft or issued statement."""

        statement: PatientBillingStatement = (
            PatientBillingStatement.objects.select_for_update().get(
                id=statement_id,
                account__organization_id=organization_id,
            )
        )
        if statement.status not in {
            PatientStatementStatus.DRAFT,
            PatientStatementStatus.ISSUED,
        }:
            raise PatientBillingLifecycleError(
                "Only draft or issued statements can be voided.",
            )
        statement.status = PatientStatementStatus.VOID
        statement.save(
            update_fields=(
                "status",
                "updated_at",
            ),
        )
        return statement


__all__ = ("PatientBillingStatementService",)

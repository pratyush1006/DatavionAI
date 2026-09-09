"""Patient billing statement selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.billing.patient_billing.models import PatientBillingStatement


class PatientBillingStatementSelector:
    """Provide organization-scoped statement reads through the account."""

    @staticmethod
    def queryset(*, organization_id: UUID) -> QuerySet[PatientBillingStatement]:
        """Return statements belonging to the organization."""

        return PatientBillingStatement.objects.select_related(
            "account",
            "account__patient",
            "account__organization",
        ).filter(account__organization_id=organization_id)

    @staticmethod
    def get(*, organization_id: UUID, statement_id: UUID) -> PatientBillingStatement:
        """Return one organization-scoped statement."""

        return PatientBillingStatementSelector.queryset(
            organization_id=organization_id
        ).get(id=statement_id)


__all__ = ("PatientBillingStatementSelector",)

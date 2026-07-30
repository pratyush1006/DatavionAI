"""
Customer selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.billing.accounts_receivable.models import Customer
from apps.platform.organizations.models import Organization
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class CustomerSelector:
    """
    Read-only queries for customer.
    """

    @staticmethod
    def queryset() -> QuerySet[Customer]:
        """
        Return the base customer queryset.
        """

        return Customer.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[Customer]:
        """
        Return all customer records.
        """

        return CustomerSelector.queryset()

    @staticmethod
    def get(
        *,
        customer_id: UUID,
    ) -> Customer:
        """
        Return a customer by identifier.
        """

        return get_object_or_404(
            CustomerSelector.queryset(),
            pk=customer_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Customer]:
        """
        Return all customer records for an organization.
        """

        return CustomerSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        customer_id: UUID,
    ) -> bool:
        """
        Determine whether a customer exists.
        """

        return (
            CustomerSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=customer_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of customer records for an organization.
        """

        return CustomerSelector.list_by_organization(
            organization=organization,
        ).count()


get_customers = CustomerSelector.list

get_customer_by_id = CustomerSelector.get

get_organization_customers = CustomerSelector.list_by_organization


__all__ = [
    "CustomerSelector",
    "get_customer_by_id",
    "get_customers",
    "get_organization_customers",
]

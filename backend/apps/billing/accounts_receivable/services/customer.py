"""
Customer services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.billing.accounts_receivable.models import Customer
from django.db import transaction


class CustomerService:
    """
    Application service for customer write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> Customer:
        """
        Create a new customer.
        """

        instance = Customer(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Customer,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> Customer:
        """
        Update an existing customer.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Customer,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a customer.
        """

        instance.hard_delete()


create_customer = CustomerService.create

update_customer = CustomerService.update

delete_customer = CustomerService.delete


__all__ = [
    "CustomerService",
    "create_customer",
    "update_customer",
    "delete_customer",
]

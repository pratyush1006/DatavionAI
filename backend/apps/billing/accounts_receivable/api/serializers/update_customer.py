"""
Update serializer for the Customer model.
"""

from __future__ import annotations

from apps.billing.accounts_receivable.models import Customer
from apps.billing.accounts_receivable.services import update_customer

from .base_customer import CustomerBaseSerializer
from .fields_customer import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class CustomerUpdateSerializer(CustomerBaseSerializer):
    """
    Serializer used for updating customer records.
    """

    class Meta(CustomerBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: Customer,
        validated_data: dict[str, object],
    ) -> Customer:
        """
        Update a customer.
        """

        return update_customer(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "CustomerUpdateSerializer",
]

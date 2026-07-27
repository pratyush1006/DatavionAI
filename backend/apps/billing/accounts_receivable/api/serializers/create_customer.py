"""
Create serializer for the Customer model.
"""

from __future__ import annotations

from apps.billing.accounts_receivable.services import create_customer

from .base_customer import CustomerBaseSerializer
from .fields_customer import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class CustomerCreateSerializer(CustomerBaseSerializer):
    """
    Serializer used for creating customer records.
    """

    class Meta(CustomerBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a customer.
        """

        return create_customer(
            validated_data=validated_data,
        )


__all__ = [
    "CustomerCreateSerializer",
]

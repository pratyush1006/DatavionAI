"""
List serializer for the Customer model.
"""

from __future__ import annotations

from .base_customer import CustomerBaseSerializer
from .fields_customer import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class CustomerListSerializer(CustomerBaseSerializer):
    """
    Serializer used for listing customer records.
    """

    class Meta(CustomerBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "CustomerListSerializer",
]

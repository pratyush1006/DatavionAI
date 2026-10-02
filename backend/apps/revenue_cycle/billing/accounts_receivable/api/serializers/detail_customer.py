"""
Detail serializer for the Customer model.
"""

from __future__ import annotations

from .base_customer import CustomerBaseSerializer
from .fields_customer import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class CustomerDetailSerializer(CustomerBaseSerializer):
    """
    Serializer used for retrieving customer details.
    """

    class Meta(CustomerBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "CustomerDetailSerializer",
]

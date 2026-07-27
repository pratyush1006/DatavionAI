"""
Address serializers.
"""

from .create import AddressCreateSerializer
from .detail import AddressDetailSerializer
from .list import AddressListSerializer
from .update import AddressUpdateSerializer

__all__ = [
    "AddressCreateSerializer",
    "AddressDetailSerializer",
    "AddressListSerializer",
    "AddressUpdateSerializer",
]

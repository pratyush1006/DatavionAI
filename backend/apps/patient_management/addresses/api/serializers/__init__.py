"""
Patient Address API serializers.
"""

from apps.patient_management.addresses.api.serializers.create import (
    AddressCreateSerializer,
)
from apps.patient_management.addresses.api.serializers.detail import (
    AddressDetailSerializer,
)
from apps.patient_management.addresses.api.serializers.list import (
    AddressListSerializer,
)
from apps.patient_management.addresses.api.serializers.update import (
    AddressUpdateSerializer,
)

__all__ = (
    "AddressCreateSerializer",
    "AddressDetailSerializer",
    "AddressListSerializer",
    "AddressUpdateSerializer",
)

"""
Patient Address API views.
"""

from apps.patient_management.addresses.api.views.lifecycle import (
    AddressActivateAPIView,
    AddressDeactivateAPIView,
    AddressSetPrimaryAPIView,
    AddressVerifyAPIView,
)
from apps.patient_management.addresses.api.views.list_create import (
    AddressListCreateAPIView,
)
from apps.patient_management.addresses.api.views.retrieve_update_destroy import (
    AddressRetrieveUpdateDestroyAPIView,
)

__all__ = (
    "AddressActivateAPIView",
    "AddressDeactivateAPIView",
    "AddressListCreateAPIView",
    "AddressRetrieveUpdateDestroyAPIView",
    "AddressSetPrimaryAPIView",
    "AddressVerifyAPIView",
)

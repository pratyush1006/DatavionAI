"""
Emergency Contacts API views.
"""

from .lifecycle import (
    EmergencyContactActivateAPIView,
    EmergencyContactBlockAPIView,
    EmergencyContactDeactivateAPIView,
    EmergencyContactSetPrimaryAPIView,
    EmergencyContactVerifyAPIView,
)
from .list_create import EmergencyContactListCreateAPIView
from .retrieve_update_destroy import (
    EmergencyContactRetrieveUpdateDestroyAPIView,
)

__all__ = (
    "EmergencyContactActivateAPIView",
    "EmergencyContactBlockAPIView",
    "EmergencyContactDeactivateAPIView",
    "EmergencyContactListCreateAPIView",
    "EmergencyContactRetrieveUpdateDestroyAPIView",
    "EmergencyContactSetPrimaryAPIView",
    "EmergencyContactVerifyAPIView",
)

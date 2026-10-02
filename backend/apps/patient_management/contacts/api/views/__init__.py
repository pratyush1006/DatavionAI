"""
Patient Contact API views.

Central export point for the Contacts API view package.
"""

from apps.patient_management.contacts.api.views.lifecycle import (
    ContactActivateAPIView,
    ContactDeactivateAPIView,
    ContactSetPrimaryAPIView,
    ContactVerifyAPIView,
)
from apps.patient_management.contacts.api.views.list_create import (
    ContactListCreateAPIView,
)
from apps.patient_management.contacts.api.views.retrieve_update_destroy import (
    ContactRetrieveUpdateDestroyAPIView,
)

__all__ = (
    "ContactActivateAPIView",
    "ContactDeactivateAPIView",
    "ContactListCreateAPIView",
    "ContactRetrieveUpdateDestroyAPIView",
    "ContactSetPrimaryAPIView",
    "ContactVerifyAPIView",
)

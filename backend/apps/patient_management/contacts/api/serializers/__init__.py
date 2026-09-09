"""
Patient Contacts API serializers.
"""

from apps.patient_management.contacts.api.serializers.create import (
    ContactCreateSerializer,
)
from apps.patient_management.contacts.api.serializers.detail import (
    ContactDetailSerializer,
)
from apps.patient_management.contacts.api.serializers.list import (
    ContactListSerializer,
)
from apps.patient_management.contacts.api.serializers.update import (
    ContactUpdateSerializer,
)

__all__ = (
    "ContactCreateSerializer",
    "ContactDetailSerializer",
    "ContactListSerializer",
    "ContactUpdateSerializer",
)

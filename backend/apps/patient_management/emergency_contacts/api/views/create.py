"""
Create API for Emergency Contacts.
"""

from __future__ import annotations

from apps.common.api import BaseCreateAPIView

from ..serializers import (
    EmergencyContactCreateSerializer,
)


class EmergencyContactCreateAPIView(
    BaseCreateAPIView,
):
    """
    Create emergency contact.
    """

    serializer_class = EmergencyContactCreateSerializer

"""
Update API for Emergency Contacts.
"""

from __future__ import annotations

from apps.common.api import (
    BaseUpdateAPIView,
)

from ...models import (
    EmergencyContact,
)
from ..serializers import (
    EmergencyContactUpdateSerializer,
)


class EmergencyContactUpdateAPIView(
    BaseUpdateAPIView,
):
    """
    Update emergency contact.
    """

    queryset = EmergencyContact.objects.all()

    serializer_class = EmergencyContactUpdateSerializer

    lookup_field = "id"

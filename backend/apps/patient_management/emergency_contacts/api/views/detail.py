"""
Retrieve API for Emergency Contacts.
"""

from __future__ import annotations

from apps.common.api import (
    BaseRetrieveAPIView,
)

from ...models import (
    EmergencyContact,
)
from ..serializers import (
    EmergencyContactDetailSerializer,
)


class EmergencyContactRetrieveAPIView(
    BaseRetrieveAPIView,
):
    """
    Retrieve emergency contact.
    """

    queryset = EmergencyContact.objects.all()

    serializer_class = EmergencyContactDetailSerializer

    lookup_field = "id"

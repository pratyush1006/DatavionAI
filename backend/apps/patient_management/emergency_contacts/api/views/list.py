"""
List API for Emergency Contacts.
"""

from __future__ import annotations

from apps.common.api import BaseListAPIView

from ...api.filters import (
    EmergencyContactFilter,
)
from ...models import (
    EmergencyContact,
)
from ..serializers import (
    EmergencyContactListSerializer,
)


class EmergencyContactListAPIView(
    BaseListAPIView,
):
    """
    List emergency contacts.
    """

    queryset = EmergencyContact.objects.all()

    serializer_class = EmergencyContactListSerializer

    filterset_class = EmergencyContactFilter

    ordering_fields = (
        "priority_order",
        "first_name",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "mobile_number",
        "email",
        "emergency_contact_number",
    )

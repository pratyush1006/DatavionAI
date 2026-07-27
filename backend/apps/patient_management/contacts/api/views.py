"""
API views for the Contacts module.
"""

from __future__ import annotations

from apps.common.api.base import (
    BaseCreateAPIView,
    BaseDestroyAPIView,
    BaseListAPIView,
    BaseRetrieveAPIView,
    BaseUpdateAPIView,
)
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
from apps.patient_management.contacts.models import Contact


class ContactListAPIView(BaseListAPIView):
    """List contacts."""

    queryset = Contact.objects.all()
    serializer_class = ContactListSerializer


class ContactRetrieveAPIView(BaseRetrieveAPIView):
    """Retrieve a contact."""

    queryset = Contact.objects.all()
    serializer_class = ContactDetailSerializer


class ContactCreateAPIView(BaseCreateAPIView):
    """Create a contact."""

    queryset = Contact.objects.all()
    serializer_class = ContactCreateSerializer


class ContactUpdateAPIView(BaseUpdateAPIView):
    """Update a contact."""

    queryset = Contact.objects.all()
    serializer_class = ContactUpdateSerializer


class ContactDestroyAPIView(BaseDestroyAPIView):
    """Delete a contact."""

    queryset = Contact.objects.all()

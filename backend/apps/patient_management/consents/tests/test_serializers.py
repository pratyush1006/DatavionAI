"""
Serializer tests for the Patient Consents module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.consents.api.serializers import (
    ConsentCreateSerializer,
    ConsentDetailSerializer,
    ConsentListSerializer,
    ConsentUpdateSerializer,
)
from apps.patient_management.consents.tests.factories import (
    ConsentFactory,
)

pytestmark = pytest.mark.django_db


def test_create_serializer():
    serializer = ConsentCreateSerializer()

    assert serializer is not None


def test_update_serializer():
    serializer = ConsentUpdateSerializer()

    assert serializer is not None


def test_list_serializer():
    consent = ConsentFactory()

    serializer = ConsentListSerializer(consent)

    assert serializer.data["id"] == str(consent.id)


def test_detail_serializer():
    consent = ConsentFactory()

    serializer = ConsentDetailSerializer(consent)

    assert serializer.data["id"] == str(consent.id)

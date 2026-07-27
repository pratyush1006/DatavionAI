"""
Model tests for Patient Consents.
"""

from __future__ import annotations

import pytest

from apps.patient_management.consents.tests.factories import (
    ConsentFactory,
)

pytestmark = pytest.mark.django_db


def test_create_consent():
    consent = ConsentFactory()

    assert consent.id is not None


def test_string_representation():
    consent = ConsentFactory()

    assert consent.consent_number in str(consent)


def test_default_version():
    consent = ConsentFactory()

    assert consent.version == 1


def test_default_status():
    consent = ConsentFactory()

    assert consent.status == "DRAFT"


def test_default_is_active():
    consent = ConsentFactory()

    assert consent.is_active is True


def test_soft_delete():
    consent = ConsentFactory()

    consent.delete()

    assert consent.is_deleted is True


def test_restore():
    consent = ConsentFactory()

    consent.delete()

    consent.restore()

    assert consent.is_deleted is False

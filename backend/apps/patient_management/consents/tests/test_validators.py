"""
Validator tests for the Patient Consents module.
"""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.patient_management.consents.validators import (
    validate_consent_title,
    validate_effective_date,
    validate_expiry_date,
    validate_version,
)

pytestmark = pytest.mark.django_db


def test_validate_title():
    validate_consent_title(
        "Treatment Consent",
    )


def test_invalid_title():
    with pytest.raises(
        ValidationError,
    ):
        validate_consent_title(
            "",
        )


def test_validate_version():
    validate_version(
        1,
    )


def test_invalid_version():
    with pytest.raises(
        ValidationError,
    ):
        validate_version(
            0,
        )


def test_validate_effective_date():
    validate_effective_date(
        timezone.localdate(),
    )


def test_invalid_effective_date():
    with pytest.raises(
        ValidationError,
    ):
        validate_effective_date(
            timezone.localdate() - timedelta(days=1),
        )


def test_validate_expiry_date():
    today = timezone.localdate()

    validate_expiry_date(
        today,
        today + timedelta(days=30),
    )


def test_invalid_expiry_date():
    today = timezone.localdate()

    with pytest.raises(
        ValidationError,
    ):
        validate_expiry_date(
            today,
            today,
        )

"""
Validator tests for the Family Members module.
"""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.patient_management.family_members.validators import (
    validate_date_of_birth,
    validate_email_address,
    validate_family_member_name,
    validate_mobile_number,
)

pytestmark = pytest.mark.django_db


def test_validate_name():
    validate_family_member_name(
        "John Doe",
    )


def test_invalid_name():
    with pytest.raises(
        ValidationError,
    ):
        validate_family_member_name(
            "123456",
        )


def test_validate_mobile():
    validate_mobile_number(
        "+919876543210",
    )


def test_invalid_mobile():
    with pytest.raises(
        ValidationError,
    ):
        validate_mobile_number(
            "abcd",
        )


def test_validate_email():
    validate_email_address(
        "john@example.com",
    )


def test_invalid_email():
    with pytest.raises(
        ValidationError,
    ):
        validate_email_address(
            "invalid-email",
        )


def test_future_date_of_birth():
    with pytest.raises(
        ValidationError,
    ):
        validate_date_of_birth(
            timezone.localdate() + timedelta(days=1),
        )

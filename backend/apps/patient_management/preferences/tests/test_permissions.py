"""
Permission tests for the Patient Preferences module.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from apps.patient_management.preferences.permissions import (
    CanCreateCommunicationPreference,
    CanCreatePatientPreference,
    CanDeleteCommunicationPreference,
    CanDeletePatientPreference,
    CanUpdateCommunicationPreference,
    CanUpdatePatientPreference,
    CanViewCommunicationPreference,
    CanViewPatientPreference,
)


class DummyUser:
    """
    Dummy user for permission testing.
    """

    def __init__(
        self,
        *,
        allowed_permissions: set[str] | None = None,
    ) -> None:
        self.allowed_permissions = allowed_permissions or set()

    def has_perm(
        self,
        permission: str,
    ) -> bool:
        return permission in self.allowed_permissions


@pytest.fixture
def view():
    """
    Dummy DRF view.
    """
    return SimpleNamespace()


def build_request(
    *permissions: str,
):
    """
    Build a request object.
    """
    return SimpleNamespace(
        user=DummyUser(
            allowed_permissions=set(
                permissions,
            ),
        ),
    )


class TestPatientPreferencePermissions:
    """
    Tests for PatientPreference permissions.
    """

    @pytest.mark.parametrize(
        (
            "permission_class",
            "permission_name",
        ),
        [
            (
                CanViewPatientPreference,
                "preferences.view_patientpreference",
            ),
            (
                CanCreatePatientPreference,
                "preferences.add_patientpreference",
            ),
            (
                CanUpdatePatientPreference,
                "preferences.change_patientpreference",
            ),
            (
                CanDeletePatientPreference,
                "preferences.delete_patientpreference",
            ),
        ],
    )
    def test_permission_granted(
        self,
        permission_class,
        permission_name,
        view,
    ) -> None:
        permission = permission_class()

        request = build_request(
            permission_name,
        )

        assert permission.has_permission(
            request,
            view,
        )

    @pytest.mark.parametrize(
        "permission_class",
        [
            CanViewPatientPreference,
            CanCreatePatientPreference,
            CanUpdatePatientPreference,
            CanDeletePatientPreference,
        ],
    )
    def test_permission_denied(
        self,
        permission_class,
        view,
    ) -> None:
        permission = permission_class()

        request = build_request()

        assert (
            permission.has_permission(
                request,
                view,
            )
            is False
        )


class TestCommunicationPreferencePermissions:
    """
    Tests for communication preference permissions.
    """

    @pytest.mark.parametrize(
        (
            "permission_class",
            "permission_name",
        ),
        [
            (
                CanViewCommunicationPreference,
                "preferences.view_patientcommunicationpreference",
            ),
            (
                CanCreateCommunicationPreference,
                "preferences.add_patientcommunicationpreference",
            ),
            (
                CanUpdateCommunicationPreference,
                "preferences.change_patientcommunicationpreference",
            ),
            (
                CanDeleteCommunicationPreference,
                "preferences.delete_patientcommunicationpreference",
            ),
        ],
    )
    def test_permission_granted(
        self,
        permission_class,
        permission_name,
        view,
    ) -> None:
        permission = permission_class()

        request = build_request(
            permission_name,
        )

        assert permission.has_permission(
            request,
            view,
        )

    @pytest.mark.parametrize(
        "permission_class",
        [
            CanViewCommunicationPreference,
            CanCreateCommunicationPreference,
            CanUpdateCommunicationPreference,
            CanDeleteCommunicationPreference,
        ],
    )
    def test_permission_denied(
        self,
        permission_class,
        view,
    ) -> None:
        permission = permission_class()

        request = build_request()

        assert (
            permission.has_permission(
                request,
                view,
            )
            is False
        )

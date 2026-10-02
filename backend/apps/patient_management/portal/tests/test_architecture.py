"""
Architecture tests for Patient Portal.
"""

from __future__ import annotations

from apps.patient_management.patients.models import Patient
from apps.patient_management.portal.constants import (
    ALLOWED_STATUS_TRANSITIONS,
)
from apps.patient_management.portal.models import PatientPortalAccount
from apps.patient_management.portal.services import PatientPortalInvitationWorkflow


def test_portal_uses_canonical_patient() -> None:
    """Verify the portal account points to the canonical Patient model."""

    patient_field = PatientPortalAccount._meta.get_field("patient")

    assert patient_field.remote_field.model is Patient


def test_portal_registers_invitation_workflow() -> None:
    """Verify the invitation workflow has a stable workflow name."""

    assert PatientPortalInvitationWorkflow.workflow_name == "patient_portal.invite"


def test_portal_has_strict_lifecycle() -> None:
    """Verify terminal deactivated accounts have no outgoing transitions."""

    assert ALLOWED_STATUS_TRANSITIONS["DEACTIVATED"] == set()


__all__ = ()

"""
Permission tests for the Patient Consents module.
"""

from __future__ import annotations

from apps.patient_management.consents.permissions import (
    ConsentPermission,
)


def test_permission_constants():
    assert ConsentPermission.CREATE == "patient_management.consents.create"

    assert ConsentPermission.UPDATE == "patient_management.consents.update"

    assert ConsentPermission.DELETE == "patient_management.consents.delete"

    assert ConsentPermission.GRANT == "patient_management.consents.grant"

    assert ConsentPermission.REVOKE == "patient_management.consents.revoke"

    assert ConsentPermission.WITHDRAW == "patient_management.consents.withdraw"

    assert ConsentPermission.EXPIRE == "patient_management.consents.expire"

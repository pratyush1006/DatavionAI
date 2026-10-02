"""Patient Address workflow registry."""

from __future__ import annotations

WORKFLOWS = {
    "create": "apps.patient_management.addresses.workflows.lifecycle.create_address",
    "update": "apps.patient_management.addresses.workflows.lifecycle.update_address",
    "delete": "apps.patient_management.addresses.workflows.lifecycle.delete_address",
    "verify": "apps.patient_management.addresses.workflows.lifecycle.verify_address",
}

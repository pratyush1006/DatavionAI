"""
Constants used by the Audit application.
"""

from __future__ import annotations

from django.db import models

# ============================================================================
# Audit Actions
# ============================================================================


class AuditAction(
    models.TextChoices,
):
    """
    Supported audit actions.
    """

    CREATE = "CREATE", "Create"
    UPDATE = "UPDATE", "Update"
    DELETE = "DELETE", "Delete"

    LOGIN = "LOGIN", "Login"
    LOGOUT = "LOGOUT", "Logout"

    APPROVE = "APPROVE", "Approve"
    REJECT = "REJECT", "Reject"

    EXPORT = "EXPORT", "Export"
    IMPORT = "IMPORT", "Import"

    RESTORE = "RESTORE", "Restore"


# ============================================================================
# Audit Modules
# ============================================================================


class AuditModule(
    models.TextChoices,
):
    """
    Platform modules that generate audit events.
    """

    ACCOUNTS = "accounts", "Accounts"
    ORGANIZATIONS = "organizations", "Organizations"
    RBAC = "rbac", "RBAC"

    DEPARTMENTS = "departments", "Departments"
    TEAMS = "teams", "Teams"
    EMPLOYEES = "employees", "Employees"

    NOTIFICATIONS = "notifications", "Notifications"
    AUDIT = "audit", "Audit"

    PATIENTS = "patients", "Patients"
    APPOINTMENTS = "appointments", "Appointments"
    ENCOUNTERS = "encounters", "Encounters"

    LABORATORIES = "laboratories", "Laboratories"
    MEDICATIONS = "medications", "Medications"
    PRESCRIPTIONS = "prescriptions", "Prescriptions"

    ALLERGIES = "allergies", "Allergies"
    DIAGNOSES = "diagnoses", "Diagnoses"
    VITALS = "vitals", "Vitals"


# ============================================================================
# Audit Event Types
# ============================================================================


class AuditEventType(
    models.TextChoices,
):
    """
    High-level audit event categories.
    """

    AUTHENTICATION = (
        "AUTHENTICATION",
        "Authentication",
    )

    AUTHORIZATION = (
        "AUTHORIZATION",
        "Authorization",
    )

    DATA_CHANGE = (
        "DATA_CHANGE",
        "Data Change",
    )

    SYSTEM = (
        "SYSTEM",
        "System",
    )


__all__ = [
    "AuditAction",
    "AuditModule",
    "AuditEventType",
]

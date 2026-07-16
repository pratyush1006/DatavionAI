"""
Permission constants.

Defines standard permission modules, actions, scopes,
and system roles for the DatavionAI authorization platform.
"""

from __future__ import annotations

from django.db import models


class PermissionModule(
    models.TextChoices,
):
    """
    Application modules.
    """

    ACCOUNTS = "accounts", "Accounts"
    ORGANIZATIONS = "organizations", "Organizations"
    RBAC = "rbac", "Role Based Access Control"
    PATIENTS = "patients", "Patients"
    PROVIDERS = "providers", "Providers"
    EMPLOYEES = "employees", "Employees"
    DEPARTMENTS = "departments", "Departments"
    TEAMS = "teams", "Teams"
    APPOINTMENTS = "appointments", "Appointments"
    ENCOUNTERS = "encounters", "Encounters"
    LABORATORIES = "laboratories", "Laboratories"
    MEDICATIONS = "medications", "Medications"
    PRESCRIPTIONS = "prescriptions", "Prescriptions"
    ALLERGIES = "allergies", "Allergies"
    DIAGNOSES = "diagnoses", "Diagnoses"
    VITALS = "vitals", "Vitals"
    PHARMACY = "pharmacy", "Pharmacy"
    BILLING = "billing", "Billing"
    INVENTORY = "inventory", "Inventory"
    NOTIFICATIONS = "notifications", "Notifications"
    AUDIT = "audit", "Audit"
    REPORTS = "reports", "Reports"
    DASHBOARD = "dashboard", "Dashboard"
    SETTINGS = "settings", "Settings"
    AI = "ai", "Artificial Intelligence"


class PermissionAction(
    models.TextChoices,
):
    """
    Permission actions.
    """

    VIEW = "view", "View"
    CREATE = "create", "Create"
    UPDATE = "update", "Update"
    DELETE = "delete", "Delete"
    APPROVE = "approve", "Approve"
    ASSIGN = "assign", "Assign"
    VERIFY = "verify", "Verify"
    RELEASE = "release", "Release"
    SIGN = "sign", "Sign"
    UPLOAD = "upload", "Upload"
    DOWNLOAD = "download", "Download"
    EXPORT = "export", "Export"
    IMPORT = "import", "Import"
    SHARE = "share", "Share"
    PRINT = "print", "Print"


class PermissionScope(
    models.TextChoices,
):
    """
    Permission scopes.
    """

    SELF = "self", "Self"
    ASSIGNED = "assigned", "Assigned"
    DEPARTMENT = "department", "Department"
    ORGANIZATION = "organization", "Organization"
    NETWORK = "network", "Network"
    ANY = "any", "Any"


class SystemRole(
    models.TextChoices,
):
    """
    Built-in system roles.
    """

    PLATFORM_ADMIN = "platform_admin", "Platform Administrator"
    ORGANIZATION_OWNER = "organization_owner", "Organization Owner"
    ORGANIZATION_ADMIN = "organization_admin", "Organization Administrator"
    DOCTOR = "doctor", "Doctor"
    CONSULTANT = "consultant", "Consultant"
    NURSE = "nurse", "Nurse"
    LABORATORY_MANAGER = "laboratory_manager", "Laboratory Manager"
    LABORATORY_TECHNICIAN = (
        "laboratory_technician",
        "Laboratory Technician",
    )
    PHARMACIST = "pharmacist", "Pharmacist"
    RECEPTIONIST = "receptionist", "Receptionist"
    PATIENT = "patient", "Patient"
    AI_AGENT = "ai_agent", "AI Agent"


__all__ = [
    "PermissionAction",
    "PermissionModule",
    "PermissionScope",
    "SystemRole",
]

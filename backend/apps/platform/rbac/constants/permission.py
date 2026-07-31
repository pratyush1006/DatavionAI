"""
Permission constants.

Defines standard permission modules, actions, scopes,
and system roles for the DatavionOS authorization platform.

Design principles:

- Multi-tenant SaaS RBAC
- Healthcare enterprise workflows
- Shared permission vocabulary
- Module.action permission naming
- Extensible lifecycle authorization
"""

from __future__ import annotations

from django.db import models


class PermissionModule(
    models.TextChoices,
):
    """
    Application modules.
    """

    ACCOUNTS = (
        "accounts",
        "Accounts",
    )

    ORGANIZATIONS = (
        "organizations",
        "Organizations",
    )

    RBAC = (
        "rbac",
        "Role Based Access Control",
    )

    # ==========================================================
    # Organization Operations
    # ==========================================================

    PATIENTS = (
        "patients",
        "Patients",
    )

    PROVIDERS = (
        "providers",
        "Providers",
    )

    EMPLOYEES = (
        "employees",
        "Employees",
    )

    DEPARTMENTS = (
        "departments",
        "Departments",
    )

    TEAMS = (
        "teams",
        "Teams",
    )

    # ==========================================================
    # Clinical Modules
    # ==========================================================

    DOCUMENTS = (
        "documents",
        "Documents",
    )

    APPOINTMENTS = (
        "appointments",
        "Appointments",
    )

    ENCOUNTERS = (
        "encounters",
        "Encounters",
    )

    LABORATORIES = (
        "laboratories",
        "Laboratories",
    )

    MEDICATIONS = (
        "medications",
        "Medications",
    )

    PRESCRIPTIONS = (
        "prescriptions",
        "Prescriptions",
    )

    ALLERGIES = (
        "allergies",
        "Allergies",
    )

    DIAGNOSES = (
        "diagnoses",
        "Diagnoses",
    )

    VITALS = (
        "vitals",
        "Vitals",
    )

    PHARMACY = (
        "pharmacy",
        "Pharmacy",
    )

    # ==========================================================
    # Enterprise Modules
    # ==========================================================

    BILLING = (
        "billing",
        "Billing",
    )

    INVENTORY = (
        "inventory",
        "Inventory",
    )

    NOTIFICATIONS = (
        "notifications",
        "Notifications",
    )

    AUDIT = (
        "audit",
        "Audit",
    )

    REPORTS = (
        "reports",
        "Reports",
    )

    DASHBOARD = (
        "dashboard",
        "Dashboard",
    )

    SETTINGS = (
        "settings",
        "Settings",
    )

    AI = (
        "ai",
        "Artificial Intelligence",
    )


class PermissionAction(
    models.TextChoices,
):
    """
    Permission actions.

    Permissions follow:

        module.action

    Examples:

        employees.create
        employees.assign
        employees.contract
        patients.view
    """

    # ==========================================================
    # CRUD
    # ==========================================================

    VIEW = (
        "view",
        "View",
    )

    CREATE = (
        "create",
        "Create",
    )

    UPDATE = (
        "update",
        "Update",
    )

    DELETE = (
        "delete",
        "Delete",
    )

    # ==========================================================
    # Lifecycle
    # ==========================================================

    ACTIVATE = (
        "activate",
        "Activate",
    )

    DEACTIVATE = (
        "deactivate",
        "Deactivate",
    )

    SUSPEND = (
        "suspend",
        "Suspend",
    )

    RESTORE = (
        "restore",
        "Restore",
    )

    # ==========================================================
    # Approval / Assignment
    # ==========================================================

    APPROVE = (
        "approve",
        "Approve",
    )

    ASSIGN = (
        "assign",
        "Assign",
    )

    # ==========================================================
    # Employee / HR Workflow Actions
    #
    # Generates:
    #
    # employees.contract
    # employees.onboard
    # employees.offboard
    #
    # ==========================================================

    CONTRACT = (
        "contract",
        "Manage Contract",
    )

    ONBOARD = (
        "onboard",
        "Onboard Employee",
    )

    OFFBOARD = (
        "offboard",
        "Offboard Employee",
    )

    # ==========================================================
    # Clinical Workflow
    # ==========================================================

    VERIFY = (
        "verify",
        "Verify",
    )

    RELEASE = (
        "release",
        "Release",
    )

    SIGN = (
        "sign",
        "Sign",
    )

    # ==========================================================
    # Document Actions
    # ==========================================================

    UPLOAD = (
        "upload",
        "Upload",
    )

    DOWNLOAD = (
        "download",
        "Download",
    )

    EXPORT = (
        "export",
        "Export",
    )

    IMPORT = (
        "import",
        "Import",
    )

    SHARE = (
        "share",
        "Share",
    )

    PRINT = (
        "print",
        "Print",
    )


class PermissionScope(
    models.TextChoices,
):
    """
    Permission scopes.
    """

    SELF = (
        "self",
        "Self",
    )

    ASSIGNED = (
        "assigned",
        "Assigned",
    )

    DEPARTMENT = (
        "department",
        "Department",
    )

    ORGANIZATION = (
        "organization",
        "Organization",
    )

    NETWORK = (
        "network",
        "Network",
    )

    ANY = (
        "any",
        "Any",
    )


class SystemRole(
    models.TextChoices,
):
    """
    Built-in system roles.
    """

    PLATFORM_ADMIN = (
        "platform_admin",
        "Platform Administrator",
    )

    ORGANIZATION_OWNER = (
        "organization_owner",
        "Organization Owner",
    )

    ORGANIZATION_ADMIN = (
        "organization_admin",
        "Organization Administrator",
    )

    DOCTOR = (
        "doctor",
        "Doctor",
    )

    CONSULTANT = (
        "consultant",
        "Consultant",
    )

    NURSE = (
        "nurse",
        "Nurse",
    )

    LABORATORY_MANAGER = (
        "laboratory_manager",
        "Laboratory Manager",
    )

    LABORATORY_TECHNICIAN = (
        "laboratory_technician",
        "Laboratory Technician",
    )

    PHARMACIST = (
        "pharmacist",
        "Pharmacist",
    )

    RECEPTIONIST = (
        "receptionist",
        "Receptionist",
    )

    PATIENT = (
        "patient",
        "Patient",
    )

    AI_AGENT = (
        "ai_agent",
        "AI Agent",
    )


__all__ = [
    "PermissionAction",
    "PermissionModule",
    "PermissionScope",
    "SystemRole",
]

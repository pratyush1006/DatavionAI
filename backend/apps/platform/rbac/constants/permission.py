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

    HR = ("hr", "Human Resources")
    ATTENDANCE = ("attendance", "Attendance")
    LEAVE = ("leave", "Leave")
    SHIFTS = ("shifts", "Shifts")
    HOLIDAYS = ("holidays", "Holidays")
    ONBOARDING = ("onboarding", "Onboarding")
    PAYROLL = ("payroll", "Payroll")
    PERFORMANCE = ("performance", "Performance")
    RECRUITMENT = ("recruitment", "Recruitment")

    HOSPITAL_OPERATIONS = ("hospital_operations", "Hospital Operations")

    DEVICES = ("devices", "Connected Devices")

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

    NURSING = ("nursing", "Nursing")

    PHARMACY = (
        "pharmacy",
        "Pharmacy",
    )

    IMAGING = ("imaging", "Imaging")

    NOTES = ("notes", "Clinical Notes")

    TRANSCRIPTION = ("transcription", "Transcription")

    # ==========================================================
    # Enterprise Modules
    # ==========================================================

    BILLING = (
        "billing",
        "Billing",
    )

    INSURANCE = (
        "insurance",
        "Insurance",
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

    DASHBOARD = ("Dashboard",)

    SETTINGS = (
        "settings",
        "Settings",
    )

    AI = (
        "ai",
        "Artificial Intelligence",
    )

    TELEMEDICINE = (
        "telemedicine",
        "Telemedicine",
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

    CANCEL = (
        "cancel",
        "Cancel",
    )

    SCHEDULE = (
        "schedule",
        "Schedule",
    )

    CONFIRM = (
        "confirm",
        "Confirm",
    )

    PREPARE = (
        "prepare",
        "Prepare",
    )

    START = (
        "start",
        "Start",
    )

    COMPLETE = (
        "complete",
        "Complete",
    )

    NO_SHOW = (
        "no_show",
        "No Show",
    )

    FAIL = (
        "fail",
        "Fail",
    )

    PARTICIPANT_MANAGE = (
        "participant.manage",
        "Manage Participants",
    )

    RECORDING_MANAGE = (
        "recording.manage",
        "Manage Recording",
    )


_TELEMEDICINE_ACTION_VALUES = frozenset(
    {
        "cancel",
        "schedule",
        "confirm",
        "prepare",
        "start",
        "complete",
        "no_show",
        "fail",
        "participant.manage",
        "recording.manage",
    }
)


def permission_actions_for(
    module: PermissionModule,
) -> tuple[PermissionAction, ...]:
    if module == PermissionModule.TELEMEDICINE:
        return tuple(PermissionAction)

    return tuple(
        action
        for action in PermissionAction
        if action.value not in _TELEMEDICINE_ACTION_VALUES
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
    PLATFORM_OWNER = ("platform_owner", "Platform Owner")
    PLATFORM_OPERATIONS = ("platform_operations", "Platform Operations")
    PLATFORM_SECURITY = ("platform_security", "Platform Security")
    PLATFORM_SUPPORT = ("platform_support", "Platform Support")
    PLATFORM_FINANCE = ("platform_finance", "Platform Finance")

    ORGANIZATION_OWNER = (
        "organization_owner",
        "Organization Owner",
    )

    ORGANIZATION_ADMIN = (
        "organization_admin",
        "Organization Administrator",
    )
    ORGANIZATION_MANAGER = ("organization_manager", "Organization Manager")

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
    THERAPIST = ("therapist", "Therapist")
    CLINICAL_MANAGER = ("clinical_manager", "Clinical Manager")

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
    PHARMACY_MANAGER = ("pharmacy_manager", "Pharmacy Manager")
    INVENTORY_MANAGER = ("inventory_manager", "Inventory Manager")

    BILLING_OFFICER = (
        "billing_officer",
        "Billing Officer",
    )

    HR_MANAGER = (
        "hr_manager",
        "HR Manager",
    )
    HR_EXECUTIVE = ("hr_executive", "HR Executive")
    ACCOUNTANT = ("accountant", "Accountant")
    FINANCE_MANAGER = ("finance_manager", "Finance Manager")
    FRONT_DESK_MANAGER = ("front_desk_manager", "Front Desk Manager")
    IMAGING_TECHNICIAN = ("imaging_technician", "Imaging Technician")
    RADIOLOGIST = ("radiologist", "Radiologist")
    IMAGING_MANAGER = ("imaging_manager", "Imaging Manager")
    DEPARTMENT_MANAGER = ("department_manager", "Department Manager")
    TEAM_LEAD = ("team_lead", "Team Lead")
    TELEMEDICINE_DOCTOR = ("telemedicine_doctor", "Telemedicine Doctor")

    RECEPTIONIST = (
        "receptionist",
        "Receptionist",
    )

    PATIENT = (
        "patient",
        "Patient",
    )
    FAMILY_CAREGIVER = ("family_caregiver", "Family Member / Caregiver")
    SUPPORT_AGENT = ("support_agent", "Support Agent")

    AI_AGENT = (
        "ai_agent",
        "AI Agent",
    )


__all__ = [
    "PermissionAction",
    "PermissionModule",
    "permission_actions_for",
    "PermissionScope",
    "SystemRole",
]

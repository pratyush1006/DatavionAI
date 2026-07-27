"""
Constants used by the Audit application.

DatavionOS enterprise audit taxonomy.

Supports:

- Authentication auditing
- Authorization auditing
- Healthcare PHI auditing
- AI governance auditing
- Security compliance
- Data lifecycle tracking
- Workflow auditing
- Enterprise SaaS compliance
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

    # ------------------------------------------------------------------
    # Data lifecycle
    # ------------------------------------------------------------------

    CREATE = (
        "CREATE",
        "Create",
    )

    UPDATE = (
        "UPDATE",
        "Update",
    )

    DELETE = (
        "DELETE",
        "Delete",
    )

    RESTORE = (
        "RESTORE",
        "Restore",
    )

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    LOGIN = (
        "LOGIN",
        "Login",
    )

    LOGOUT = (
        "LOGOUT",
        "Logout",
    )

    FAILED_LOGIN = (
        "FAILED_LOGIN",
        "Failed Login",
    )

    PASSWORD_RESET = (
        "PASSWORD_RESET",
        "Password Reset",
    )

    # ------------------------------------------------------------------
    # Authorization / RBAC
    # ------------------------------------------------------------------

    APPROVE = (
        "APPROVE",
        "Approve",
    )

    REJECT = (
        "REJECT",
        "Reject",
    )

    ROLE_CHANGE = (
        "ROLE_CHANGE",
        "Role Change",
    )

    PERMISSION_CHANGE = (
        "PERMISSION_CHANGE",
        "Permission Change",
    )

    # ------------------------------------------------------------------
    # Healthcare PHI access
    # ------------------------------------------------------------------

    VIEW = (
        "VIEW",
        "View",
    )

    ACCESS = (
        "ACCESS",
        "Access",
    )

    DOWNLOAD = (
        "DOWNLOAD",
        "Download",
    )

    PRINT = (
        "PRINT",
        "Print",
    )

    SHARE = (
        "SHARE",
        "Share",
    )

    CONSENT = (
        "CONSENT",
        "Consent",
    )

    SIGN = (
        "SIGN",
        "Sign",
    )

    # ------------------------------------------------------------------
    # Data transfer
    # ------------------------------------------------------------------

    EXPORT = (
        "EXPORT",
        "Export",
    )

    IMPORT = (
        "IMPORT",
        "Import",
    )

    # ------------------------------------------------------------------
    # AI Governance
    # ------------------------------------------------------------------

    AI_ACCESS = (
        "AI_ACCESS",
        "AI Access",
    )

    AI_GENERATION = (
        "AI_GENERATION",
        "AI Generation",
    )

    AI_EXECUTION = (
        "AI_EXECUTION",
        "AI Execution",
    )

    AI_APPROVAL = (
        "AI_APPROVAL",
        "AI Approval",
    )

    AI_FEEDBACK = (
        "AI_FEEDBACK",
        "AI Feedback",
    )

    # ------------------------------------------------------------------
    # Workflow
    # ------------------------------------------------------------------

    WORKFLOW_START = (
        "WORKFLOW_START",
        "Workflow Start",
    )

    WORKFLOW_COMPLETE = (
        "WORKFLOW_COMPLETE",
        "Workflow Complete",
    )

    WORKFLOW_APPROVE = (
        "WORKFLOW_APPROVE",
        "Workflow Approve",
    )

    WORKFLOW_REJECT = (
        "WORKFLOW_REJECT",
        "Workflow Reject",
    )


# ============================================================================
# Audit Modules
# ============================================================================


class AuditModule(
    models.TextChoices,
):
    """
    Platform modules that generate audit events.
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
        "RBAC",
    )

    SUBSCRIPTIONS = (
        "subscriptions",
        "Subscriptions",
    )

    DEPARTMENTS = (
        "departments",
        "Departments",
    )

    TEAMS = (
        "teams",
        "Teams",
    )

    EMPLOYEES = (
        "employees",
        "Employees",
    )

    NOTIFICATIONS = (
        "notifications",
        "Notifications",
    )

    AUDIT = (
        "audit",
        "Audit",
    )

    # ------------------------------------------------------------------
    # Healthcare modules
    # ------------------------------------------------------------------

    PATIENTS = (
        "patients",
        "Patients",
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

    # ------------------------------------------------------------------
    # Platform capabilities
    # ------------------------------------------------------------------

    AI = (
        "ai",
        "Artificial Intelligence",
    )

    WORKFLOW = (
        "workflow",
        "Workflow",
    )

    DOCUMENTS = (
        "documents",
        "Documents",
    )

    INTEGRATIONS = (
        "integrations",
        "Integrations",
    )

    REPORTING = (
        "reporting",
        "Reporting",
    )


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

    DATA_ACCESS = (
        "DATA_ACCESS",
        "Data Access",
    )

    DATA_CHANGE = (
        "DATA_CHANGE",
        "Data Change",
    )

    AI_GOVERNANCE = (
        "AI_GOVERNANCE",
        "AI Governance",
    )

    SECURITY = (
        "SECURITY",
        "Security",
    )

    COMPLIANCE = (
        "COMPLIANCE",
        "Compliance",
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

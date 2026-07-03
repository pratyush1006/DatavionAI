"""
Constants used by the Audit application.
"""

from __future__ import annotations

# ============================================================================
# Audit Actions
# ============================================================================

AUDIT_ACTION_CREATE = "CREATE"
AUDIT_ACTION_UPDATE = "UPDATE"
AUDIT_ACTION_DELETE = "DELETE"
AUDIT_ACTION_LOGIN = "LOGIN"
AUDIT_ACTION_LOGOUT = "LOGOUT"
AUDIT_ACTION_APPROVE = "APPROVE"
AUDIT_ACTION_REJECT = "REJECT"
AUDIT_ACTION_EXPORT = "EXPORT"
AUDIT_ACTION_IMPORT = "IMPORT"
AUDIT_ACTION_RESTORE = "RESTORE"

AUDIT_ACTION_CHOICES = (
    (AUDIT_ACTION_CREATE, "Create"),
    (AUDIT_ACTION_UPDATE, "Update"),
    (AUDIT_ACTION_DELETE, "Delete"),
    (AUDIT_ACTION_LOGIN, "Login"),
    (AUDIT_ACTION_LOGOUT, "Logout"),
    (AUDIT_ACTION_APPROVE, "Approve"),
    (AUDIT_ACTION_REJECT, "Reject"),
    (AUDIT_ACTION_EXPORT, "Export"),
    (AUDIT_ACTION_IMPORT, "Import"),
    (AUDIT_ACTION_RESTORE, "Restore"),
)

# ============================================================================
# Audit Modules
# ============================================================================

AUDIT_MODULE_ACCOUNTS = "accounts"
AUDIT_MODULE_RBAC = "rbac"
AUDIT_MODULE_ORGANIZATIONS = "organizations"
AUDIT_MODULE_DEPARTMENTS = "departments"
AUDIT_MODULE_TEAMS = "teams"
AUDIT_MODULE_EMPLOYEES = "employees"
AUDIT_MODULE_AUDIT = "audit"

# ============================================================================
# Audit Event Types (Future Use)
# ============================================================================

AUDIT_EVENT_AUTHENTICATION = "AUTHENTICATION"
AUDIT_EVENT_AUTHORIZATION = "AUTHORIZATION"
AUDIT_EVENT_DATA_CHANGE = "DATA_CHANGE"
AUDIT_EVENT_SYSTEM = "SYSTEM"

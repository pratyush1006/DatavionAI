"""
Constants for the RBAC app.
"""

from __future__ import annotations

# ==========================================================
# Field Lengths
# ==========================================================

ROLE_NAME_MAX_LENGTH = 100
ROLE_CODE_MAX_LENGTH = 100

PERMISSION_NAME_MAX_LENGTH = 100
PERMISSION_CODE_MAX_LENGTH = 100

DESCRIPTION_MAX_LENGTH = 255

# ==========================================================
# Default Roles
# ==========================================================

ROLE_SUPER_ADMIN = "SUPER_ADMIN"
ROLE_ORGANIZATION_ADMIN = "ORGANIZATION_ADMIN"
ROLE_MANAGER = "MANAGER"
ROLE_EMPLOYEE = "EMPLOYEE"

DEFAULT_ROLES = (
    ROLE_SUPER_ADMIN,
    ROLE_ORGANIZATION_ADMIN,
    ROLE_MANAGER,
    ROLE_EMPLOYEE,
)

# ==========================================================
# Permission Codes
# ==========================================================

PERMISSION_VIEW = "VIEW"
PERMISSION_CREATE = "CREATE"
PERMISSION_UPDATE = "UPDATE"
PERMISSION_DELETE = "DELETE"
PERMISSION_EXPORT = "EXPORT"
PERMISSION_IMPORT = "IMPORT"

DEFAULT_PERMISSIONS = (
    PERMISSION_VIEW,
    PERMISSION_CREATE,
    PERMISSION_UPDATE,
    PERMISSION_DELETE,
    PERMISSION_EXPORT,
    PERMISSION_IMPORT,
)

# ==========================================================
# Permission Scopes
# ==========================================================

SCOPE_GLOBAL = "GLOBAL"
SCOPE_ORGANIZATION = "ORGANIZATION"
SCOPE_DEPARTMENT = "DEPARTMENT"
SCOPE_SELF = "SELF"

PERMISSION_SCOPES = (
    SCOPE_GLOBAL,
    SCOPE_ORGANIZATION,
    SCOPE_DEPARTMENT,
    SCOPE_SELF,
)

"""
Audit constants for DatavionOS.

Defines framework-wide constants for audit actions,
categories, and severity levels.
"""

from __future__ import annotations

###############################################################################
# Audit Actions
###############################################################################

ACTION_CREATE = "create"

ACTION_READ = "read"

ACTION_UPDATE = "update"

ACTION_DELETE = "delete"

ACTION_LOGIN = "login"

ACTION_LOGOUT = "logout"

ACTION_EXPORT = "export"

ACTION_IMPORT = "import"

ACTION_APPROVE = "approve"

ACTION_REJECT = "reject"


###############################################################################
# Audit Categories
###############################################################################

CATEGORY_AUTHENTICATION = "authentication"

CATEGORY_AUTHORIZATION = "authorization"

CATEGORY_DATA = "data"

CATEGORY_SECURITY = "security"

CATEGORY_CONFIGURATION = "configuration"

CATEGORY_WORKFLOW = "workflow"

CATEGORY_SYSTEM = "system"

CATEGORY_INTEGRATION = "integration"


###############################################################################
# Audit Severity Levels
###############################################################################

LEVEL_INFO = "info"

LEVEL_WARNING = "warning"

LEVEL_ERROR = "error"

LEVEL_CRITICAL = "critical"


###############################################################################
# Default Values
###############################################################################

DEFAULT_ACTION = ACTION_READ

DEFAULT_CATEGORY = CATEGORY_SYSTEM

DEFAULT_LEVEL = LEVEL_INFO


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "ACTION_APPROVE",
    "ACTION_CREATE",
    "ACTION_DELETE",
    "ACTION_EXPORT",
    "ACTION_IMPORT",
    "ACTION_LOGIN",
    "ACTION_LOGOUT",
    "ACTION_READ",
    "ACTION_REJECT",
    "ACTION_UPDATE",
    "CATEGORY_AUTHENTICATION",
    "CATEGORY_AUTHORIZATION",
    "CATEGORY_CONFIGURATION",
    "CATEGORY_DATA",
    "CATEGORY_INTEGRATION",
    "CATEGORY_SECURITY",
    "CATEGORY_SYSTEM",
    "CATEGORY_WORKFLOW",
    "DEFAULT_ACTION",
    "DEFAULT_CATEGORY",
    "DEFAULT_LEVEL",
    "LEVEL_CRITICAL",
    "LEVEL_ERROR",
    "LEVEL_INFO",
    "LEVEL_WARNING",
)

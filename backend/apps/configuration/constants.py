"""
Configuration constants.
"""

from __future__ import annotations

from typing import Final

# ==============================================================================
# Configuration Categories
# ==============================================================================

CONFIGURATION_CATEGORY_GENERAL: Final[str] = "GENERAL"
CONFIGURATION_CATEGORY_BRANDING: Final[str] = "BRANDING"
CONFIGURATION_CATEGORY_SECURITY: Final[str] = "SECURITY"
CONFIGURATION_CATEGORY_EMAIL: Final[str] = "EMAIL"
CONFIGURATION_CATEGORY_SMS: Final[str] = "SMS"
CONFIGURATION_CATEGORY_STORAGE: Final[str] = "STORAGE"
CONFIGURATION_CATEGORY_AI: Final[str] = "AI"
CONFIGURATION_CATEGORY_SYSTEM: Final[str] = "SYSTEM"

CONFIGURATION_CATEGORY_CHOICES: Final = (
    (
        CONFIGURATION_CATEGORY_GENERAL,
        "General",
    ),
    (
        CONFIGURATION_CATEGORY_BRANDING,
        "Branding",
    ),
    (
        CONFIGURATION_CATEGORY_SECURITY,
        "Security",
    ),
    (
        CONFIGURATION_CATEGORY_EMAIL,
        "Email",
    ),
    (
        CONFIGURATION_CATEGORY_SMS,
        "SMS",
    ),
    (
        CONFIGURATION_CATEGORY_STORAGE,
        "Storage",
    ),
    (
        CONFIGURATION_CATEGORY_AI,
        "Artificial Intelligence",
    ),
    (
        CONFIGURATION_CATEGORY_SYSTEM,
        "System",
    ),
)

# ==============================================================================
# Configuration Value Types
# ==============================================================================

CONFIGURATION_TYPE_STRING: Final[str] = "STRING"
CONFIGURATION_TYPE_INTEGER: Final[str] = "INTEGER"
CONFIGURATION_TYPE_BOOLEAN: Final[str] = "BOOLEAN"
CONFIGURATION_TYPE_FLOAT: Final[str] = "FLOAT"
CONFIGURATION_TYPE_JSON: Final[str] = "JSON"

CONFIGURATION_TYPE_CHOICES: Final = (
    (
        CONFIGURATION_TYPE_STRING,
        "String",
    ),
    (
        CONFIGURATION_TYPE_INTEGER,
        "Integer",
    ),
    (
        CONFIGURATION_TYPE_BOOLEAN,
        "Boolean",
    ),
    (
        CONFIGURATION_TYPE_FLOAT,
        "Float",
    ),
    (
        CONFIGURATION_TYPE_JSON,
        "JSON",
    ),
)

# ==============================================================================
# Feature Flag Status
# ==============================================================================

FEATURE_FLAG_ENABLED: Final[bool] = True
FEATURE_FLAG_DISABLED: Final[bool] = False

# ==============================================================================
# Feature Flag Keys
# ==============================================================================

FEATURE_AI_ASSISTANT: Final[str] = "AI_ASSISTANT"
FEATURE_APPOINTMENTS: Final[str] = "APPOINTMENTS"
FEATURE_AUDIT: Final[str] = "AUDIT"
FEATURE_BILLING: Final[str] = "BILLING"
FEATURE_EMPLOYEES: Final[str] = "EMPLOYEES"
FEATURE_INVENTORY: Final[str] = "INVENTORY"
FEATURE_LABORATORY: Final[str] = "LABORATORY"
FEATURE_NOTIFICATIONS: Final[str] = "NOTIFICATIONS"
FEATURE_PATIENTS: Final[str] = "PATIENTS"
FEATURE_PHARMACY: Final[str] = "PHARMACY"
FEATURE_STORAGE: Final[str] = "STORAGE"

FEATURE_FLAG_CHOICES: Final = (
    (
        FEATURE_AI_ASSISTANT,
        "AI Assistant",
    ),
    (
        FEATURE_APPOINTMENTS,
        "Appointments",
    ),
    (
        FEATURE_AUDIT,
        "Audit",
    ),
    (
        FEATURE_BILLING,
        "Billing",
    ),
    (
        FEATURE_EMPLOYEES,
        "Employees",
    ),
    (
        FEATURE_INVENTORY,
        "Inventory",
    ),
    (
        FEATURE_LABORATORY,
        "Laboratory",
    ),
    (
        FEATURE_NOTIFICATIONS,
        "Notifications",
    ),
    (
        FEATURE_PATIENTS,
        "Patients",
    ),
    (
        FEATURE_PHARMACY,
        "Pharmacy",
    ),
    (
        FEATURE_STORAGE,
        "Storage",
    ),
)

# ==============================================================================
# Default Configuration Values
# ==============================================================================

DEFAULT_PLATFORM_NAME: Final[str] = "Datavion AI"

DEFAULT_LANGUAGE: Final[str] = "en"

DEFAULT_TIMEZONE: Final[str] = "UTC"

DEFAULT_CURRENCY: Final[str] = "USD"

DEFAULT_DATE_FORMAT: Final[str] = "YYYY-MM-DD"

DEFAULT_TIME_FORMAT: Final[str] = "24H"

DEFAULT_SESSION_TIMEOUT: Final[int] = 30

DEFAULT_PASSWORD_MIN_LENGTH: Final[int] = 8

DEFAULT_LOGIN_ATTEMPTS: Final[int] = 5

# ==============================================================================
# Provider Defaults
# ==============================================================================

DEFAULT_STORAGE_PROVIDER: Final[str] = "LOCAL"

DEFAULT_AI_PROVIDER: Final[str] = "NONE"

DEFAULT_EMAIL_PROVIDER: Final[str] = "SMTP"

DEFAULT_SMS_PROVIDER: Final[str] = "NONE"

"""
DatavionAI API URL Constants.

Centralized URL prefixes, route namespaces, endpoint paths, documentation
routes, health routes, metrics routes, authentication routes, and common API
paths used throughout the DatavionAI platform.

Guidelines
----------
- Keep URLs immutable.
- Do not hardcode URLs anywhere else.
- Business module URLs belong to their respective apps.
- Runtime URL configuration belongs in settings.

Copyright (c) DatavionAI.
"""

from __future__ import annotations

from typing import Final

from .metadata import ApiVersion

###############################################################################
# Root Prefixes
###############################################################################

ROOT_PREFIX: Final[str] = "/"

API_PREFIX: Final[str] = "/api"

API_VERSION_PREFIX: Final[str] = f"{API_PREFIX}/{ApiVersion.V1.value}"

ADMIN_PREFIX: Final[str] = "/admin"

STATIC_PREFIX: Final[str] = "/static"

MEDIA_PREFIX: Final[str] = "/media"

###############################################################################
# Route Namespaces
###############################################################################

API_NAMESPACE: Final[str] = "api"

AUTH_NAMESPACE: Final[str] = "auth"

ADMIN_NAMESPACE: Final[str] = "admin"

HEALTH_NAMESPACE: Final[str] = "health"

METRICS_NAMESPACE: Final[str] = "metrics"

WEBHOOK_NAMESPACE: Final[str] = "webhooks"

###############################################################################
# Authentication
###############################################################################

AUTH_PREFIX: Final[str] = "/auth"

LOGIN_PATH: Final[str] = "/auth/login/"

LOGOUT_PATH: Final[str] = "/auth/logout/"

REGISTER_PATH: Final[str] = "/auth/register/"

REFRESH_TOKEN_PATH: Final[str] = "/auth/token/refresh/"

VERIFY_EMAIL_PATH: Final[str] = "/auth/email/verify/"

FORGOT_PASSWORD_PATH: Final[str] = "/auth/password/forgot/"

RESET_PASSWORD_PATH: Final[str] = "/auth/password/reset/"

CHANGE_PASSWORD_PATH: Final[str] = "/auth/password/change/"

###############################################################################
# Documentation
###############################################################################

OPENAPI_SCHEMA_PATH: Final[str] = "/api/schema/"

OPENAPI_JSON_PATH: Final[str] = "/api/schema/?format=json"

OPENAPI_YAML_PATH: Final[str] = "/api/schema/?format=yaml"

SWAGGER_UI_PATH: Final[str] = "/api/docs/"

REDOC_UI_PATH: Final[str] = "/api/redoc/"

POSTMAN_COLLECTION_PATH: Final[str] = "/api/postman/"

API_CHANGELOG_PATH: Final[str] = "/api/changelog/"

API_RELEASE_NOTES_PATH: Final[str] = "/api/releases/"

###############################################################################
# Health
###############################################################################

HEALTH_PREFIX: Final[str] = "/health"

HEALTH_PATH: Final[str] = "/health/"

LIVENESS_PATH: Final[str] = "/health/live/"

READINESS_PATH: Final[str] = "/health/ready/"

STARTUP_PATH: Final[str] = "/health/startup/"

###############################################################################
# Metrics
###############################################################################

METRICS_PREFIX: Final[str] = "/metrics"

METRICS_PATH: Final[str] = "/metrics/"

APPLICATION_METRICS_PATH: Final[str] = "/metrics/application/"

SYSTEM_METRICS_PATH: Final[str] = "/metrics/system/"

BUSINESS_METRICS_PATH: Final[str] = "/metrics/business/"

###############################################################################
# Diagnostics
###############################################################################

DIAGNOSTICS_PATH: Final[str] = "/diagnostics/"

SYSTEM_INFO_PATH: Final[str] = "/system/info/"

BUILD_INFO_PATH: Final[str] = "/system/build/"

VERSION_INFO_PATH: Final[str] = "/system/version/"

###############################################################################
# Webhooks
###############################################################################

WEBHOOK_PREFIX: Final[str] = "/webhooks"

WEBHOOK_PATH: Final[str] = "/webhooks/"

###############################################################################
# API Utilities
###############################################################################

PING_PATH: Final[str] = "/ping/"

STATUS_PATH: Final[str] = "/status/"

VERSION_PATH: Final[str] = "/version/"

###############################################################################
# Reserved Paths
###############################################################################

RESERVED_ENDPOINTS: Final[frozenset[str]] = frozenset(
    {
        "admin",
        "api",
        "auth",
        "docs",
        "schema",
        "health",
        "metrics",
        "webhooks",
        "static",
        "media",
    }
)

###############################################################################
# Public Endpoint Groups
###############################################################################

DOCUMENTATION_ENDPOINTS: Final[tuple[str, ...]] = (
    OPENAPI_SCHEMA_PATH,
    OPENAPI_JSON_PATH,
    OPENAPI_YAML_PATH,
    SWAGGER_UI_PATH,
    REDOC_UI_PATH,
    POSTMAN_COLLECTION_PATH,
)

HEALTH_ENDPOINTS: Final[tuple[str, ...]] = (
    HEALTH_PATH,
    LIVENESS_PATH,
    READINESS_PATH,
    STARTUP_PATH,
)

METRICS_ENDPOINTS: Final[tuple[str, ...]] = (
    METRICS_PATH,
    APPLICATION_METRICS_PATH,
    SYSTEM_METRICS_PATH,
    BUSINESS_METRICS_PATH,
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "ApiVersion",
)

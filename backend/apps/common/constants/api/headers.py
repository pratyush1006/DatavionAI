"""
DatavionAI API Header Constants.

Centralized HTTP header definitions used throughout the DatavionAI
platform.

This module defines request, response, authentication, tracing,
multi-tenant, caching, CORS, security, monitoring, webhook, and
internal service communication headers.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No business logic
- Safe to import everywhere
- RFC compliant where applicable
"""

from __future__ import annotations

from typing import Final

###############################################################################
# Standard HTTP Headers
###############################################################################

HEADER_ACCEPT: Final[str] = "Accept"

HEADER_ACCEPT_CHARSET: Final[str] = "Accept-Charset"

HEADER_ACCEPT_ENCODING: Final[str] = "Accept-Encoding"

HEADER_ACCEPT_LANGUAGE: Final[str] = "Accept-Language"

HEADER_CONTENT_TYPE: Final[str] = "Content-Type"

HEADER_CONTENT_LENGTH: Final[str] = "Content-Length"

HEADER_CONTENT_ENCODING: Final[str] = "Content-Encoding"

HEADER_CONTENT_LANGUAGE: Final[str] = "Content-Language"

HEADER_CONTENT_DISPOSITION: Final[str] = "Content-Disposition"

HEADER_TRANSFER_ENCODING: Final[str] = "Transfer-Encoding"

HEADER_HOST: Final[str] = "Host"

HEADER_ORIGIN: Final[str] = "Origin"

HEADER_REFERER: Final[str] = "Referer"

HEADER_USER_AGENT: Final[str] = "User-Agent"

###############################################################################
# Authentication Headers
###############################################################################

HEADER_AUTHORIZATION: Final[str] = "Authorization"

HEADER_BEARER: Final[str] = "Bearer"

HEADER_API_KEY: Final[str] = "X-API-Key"

HEADER_ACCESS_TOKEN: Final[str] = "X-Access-Token"

HEADER_REFRESH_TOKEN: Final[str] = "X-Refresh-Token"

HEADER_ID_TOKEN: Final[str] = "X-ID-Token"

HEADER_SESSION_ID: Final[str] = "X-Session-ID"

HEADER_DEVICE_ID: Final[str] = "X-Device-ID"

HEADER_DEVICE_NAME: Final[str] = "X-Device-Name"

HEADER_DEVICE_TYPE: Final[str] = "X-Device-Type"

HEADER_DEVICE_PLATFORM: Final[str] = "X-Device-Platform"

###############################################################################
# Identity Headers
###############################################################################

HEADER_USER_ID: Final[str] = "X-User-ID"

HEADER_USERNAME: Final[str] = "X-Username"

HEADER_ROLE: Final[str] = "X-Role"

HEADER_PERMISSIONS: Final[str] = "X-Permissions"

###############################################################################
# Multi-Tenant Headers
###############################################################################

HEADER_TENANT_ID: Final[str] = "X-Tenant-ID"

HEADER_ORGANIZATION_ID: Final[str] = "X-Organization-ID"

HEADER_ORGANIZATION_CODE: Final[str] = "X-Organization-Code"

HEADER_WORKSPACE_ID: Final[str] = "X-Workspace-ID"

HEADER_DEPARTMENT_ID: Final[str] = "X-Department-ID"

HEADER_LOCATION_ID: Final[str] = "X-Location-ID"

HEADER_BRANCH_ID: Final[str] = "X-Branch-ID"

###############################################################################
# Correlation & Distributed Tracing
###############################################################################

HEADER_REQUEST_ID: Final[str] = "X-Request-ID"

HEADER_CORRELATION_ID: Final[str] = "X-Correlation-ID"

HEADER_TRACE_ID: Final[str] = "X-Trace-ID"

HEADER_PARENT_TRACE_ID: Final[str] = "X-Parent-Trace-ID"

HEADER_SPAN_ID: Final[str] = "X-Span-ID"

HEADER_TRANSACTION_ID: Final[str] = "X-Transaction-ID"

###############################################################################
# API Versioning
###############################################################################

HEADER_API_VERSION: Final[str] = "X-API-Version"

HEADER_CLIENT_VERSION: Final[str] = "X-Client-Version"

HEADER_PLATFORM_VERSION: Final[str] = "X-Platform-Version"

###############################################################################
# Localization
###############################################################################

HEADER_LANGUAGE: Final[str] = "X-Language"

HEADER_LOCALE: Final[str] = "X-Locale"

HEADER_TIMEZONE: Final[str] = "X-Timezone"

###############################################################################
# Idempotency
###############################################################################

HEADER_IDEMPOTENCY_KEY: Final[str] = "Idempotency-Key"

###############################################################################
# Rate Limiting
###############################################################################

HEADER_RATE_LIMIT: Final[str] = "X-RateLimit-Limit"

HEADER_RATE_LIMIT_REMAINING: Final[str] = "X-RateLimit-Remaining"

HEADER_RATE_LIMIT_RESET: Final[str] = "X-RateLimit-Reset"

HEADER_RETRY_AFTER: Final[str] = "Retry-After"

###############################################################################
# Pagination
###############################################################################

HEADER_TOTAL_COUNT: Final[str] = "X-Total-Count"

HEADER_TOTAL_PAGES: Final[str] = "X-Total-Pages"

HEADER_PAGE: Final[str] = "X-Page"

HEADER_PAGE_SIZE: Final[str] = "X-Page-Size"

###############################################################################
# Conditional Requests
###############################################################################

HEADER_ETAG: Final[str] = "ETag"

HEADER_IF_MATCH: Final[str] = "If-Match"

HEADER_IF_NONE_MATCH: Final[str] = "If-None-Match"

HEADER_IF_MODIFIED_SINCE: Final[str] = "If-Modified-Since"

HEADER_LAST_MODIFIED: Final[str] = "Last-Modified"

###############################################################################
# Cache Headers
###############################################################################

HEADER_CACHE_CONTROL: Final[str] = "Cache-Control"

HEADER_EXPIRES: Final[str] = "Expires"

HEADER_PRAGMA: Final[str] = "Pragma"

HEADER_VARY: Final[str] = "Vary"

###############################################################################
# CORS Headers
###############################################################################

HEADER_ACCESS_CONTROL_ALLOW_ORIGIN: Final[str] = "Access-Control-Allow-Origin"

HEADER_ACCESS_CONTROL_ALLOW_HEADERS: Final[str] = "Access-Control-Allow-Headers"

HEADER_ACCESS_CONTROL_ALLOW_METHODS: Final[str] = "Access-Control-Allow-Methods"

HEADER_ACCESS_CONTROL_ALLOW_CREDENTIALS: Final[str] = "Access-Control-Allow-Credentials"

HEADER_ACCESS_CONTROL_EXPOSE_HEADERS: Final[str] = "Access-Control-Expose-Headers"

###############################################################################
# Security Headers
###############################################################################

HEADER_STRICT_TRANSPORT_SECURITY: Final[str] = "Strict-Transport-Security"

HEADER_CONTENT_SECURITY_POLICY: Final[str] = "Content-Security-Policy"

HEADER_X_FRAME_OPTIONS: Final[str] = "X-Frame-Options"

HEADER_X_CONTENT_TYPE_OPTIONS: Final[str] = "X-Content-Type-Options"

HEADER_REFERRER_POLICY: Final[str] = "Referrer-Policy"

HEADER_PERMISSIONS_POLICY: Final[str] = "Permissions-Policy"

HEADER_CROSS_ORIGIN_OPENER_POLICY: Final[str] = "Cross-Origin-Opener-Policy"

HEADER_CROSS_ORIGIN_RESOURCE_POLICY: Final[str] = "Cross-Origin-Resource-Policy"

HEADER_CROSS_ORIGIN_EMBEDDER_POLICY: Final[str] = "Cross-Origin-Embedder-Policy"

###############################################################################
# Monitoring
###############################################################################

HEADER_SERVER_TIMING: Final[str] = "Server-Timing"

HEADER_REQUEST_DURATION: Final[str] = "X-Request-Duration"

HEADER_TRACE_SAMPLING: Final[str] = "X-Trace-Sampling"

###############################################################################
# Webhooks
###############################################################################

HEADER_WEBHOOK_EVENT: Final[str] = "X-Webhook-Event"

HEADER_WEBHOOK_SIGNATURE: Final[str] = "X-Webhook-Signature"

HEADER_WEBHOOK_DELIVERY: Final[str] = "X-Webhook-Delivery"

HEADER_WEBHOOK_TIMESTAMP: Final[str] = "X-Webhook-Timestamp"

HEADER_WEBHOOK_RETRY: Final[str] = "X-Webhook-Retry"

###############################################################################
# Internal Platform Headers
###############################################################################

HEADER_SERVICE_NAME: Final[str] = "X-Service-Name"

HEADER_SERVICE_VERSION: Final[str] = "X-Service-Version"

HEADER_INSTANCE_ID: Final[str] = "X-Instance-ID"

HEADER_NODE_ID: Final[str] = "X-Node-ID"

###############################################################################
# Header Groups
###############################################################################

AUTH_HEADERS: Final[frozenset[str]] = frozenset(
    {
        HEADER_AUTHORIZATION,
        HEADER_API_KEY,
        HEADER_ACCESS_TOKEN,
        HEADER_REFRESH_TOKEN,
        HEADER_ID_TOKEN,
    }
)

TRACING_HEADERS: Final[frozenset[str]] = frozenset(
    {
        HEADER_REQUEST_ID,
        HEADER_CORRELATION_ID,
        HEADER_TRACE_ID,
        HEADER_PARENT_TRACE_ID,
        HEADER_SPAN_ID,
        HEADER_TRANSACTION_ID,
    }
)

TENANT_HEADERS: Final[frozenset[str]] = frozenset(
    {
        HEADER_TENANT_ID,
        HEADER_ORGANIZATION_ID,
        HEADER_ORGANIZATION_CODE,
        HEADER_WORKSPACE_ID,
        HEADER_BRANCH_ID,
        HEADER_DEPARTMENT_ID,
        HEADER_LOCATION_ID,
    }
)

CACHE_HEADERS: Final[frozenset[str]] = frozenset(
    {
        HEADER_CACHE_CONTROL,
        HEADER_ETAG,
        HEADER_EXPIRES,
        HEADER_PRAGMA,
        HEADER_VARY,
    }
)

SECURITY_HEADERS: Final[frozenset[str]] = frozenset(
    {
        HEADER_STRICT_TRANSPORT_SECURITY,
        HEADER_CONTENT_SECURITY_POLICY,
        HEADER_X_FRAME_OPTIONS,
        HEADER_X_CONTENT_TYPE_OPTIONS,
        HEADER_REFERRER_POLICY,
        HEADER_PERMISSIONS_POLICY,
        HEADER_CROSS_ORIGIN_OPENER_POLICY,
        HEADER_CROSS_ORIGIN_RESOURCE_POLICY,
        HEADER_CROSS_ORIGIN_EMBEDDER_POLICY,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper())

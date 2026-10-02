"""
Middleware framework for DatavionOS.

Provides reusable middleware components for:

- request processing
- request context
- request tracing
- correlation tracking
- security headers
- auditing
- multi-tenant SaaS isolation
"""

from __future__ import annotations

from .audit import (
    AuditMiddleware,
)
from .base import (
    BaseMiddleware,
)
from .context import (
    CORRELATION_ID_CONTEXT_KEY,
    ORGANIZATION_CONTEXT_KEY,
    REQUEST_CONTEXT_KEY,
    REQUEST_ID_CONTEXT_KEY,
    TENANT_CONTEXT_KEY,
    RequestContextMiddleware,
    clear_context,
    get_client_ip,
    get_context,
    get_correlation_id,
    get_current_organization,
    get_current_request,
    get_current_tenant,
    get_current_user,
    get_request_id,
    get_user_agent,
    set_context,
    set_correlation_id,
    set_current_organization,
    set_current_tenant,
    set_request_id,
)
from .correlation_id import (
    CorrelationIDMiddleware,
)
from .request_id import (
    RequestIDMiddleware,
)
from .security_headers import (
    SecurityHeadersMiddleware,
)
from .tenant import (
    NullTenantResolver,
    TenantMiddleware,
    TenantResolver,
)

__all__: tuple[str, ...] = (
    # Base
    "BaseMiddleware",
    # Context Middleware
    "RequestContextMiddleware",
    # Request tracing
    "RequestIDMiddleware",
    "CorrelationIDMiddleware",
    # Tenant
    "TenantMiddleware",
    "TenantResolver",
    "NullTenantResolver",
    # Security
    "SecurityHeadersMiddleware",
    # Audit
    "AuditMiddleware",
    # Context Keys
    "REQUEST_CONTEXT_KEY",
    "REQUEST_ID_CONTEXT_KEY",
    "CORRELATION_ID_CONTEXT_KEY",
    "TENANT_CONTEXT_KEY",
    "ORGANIZATION_CONTEXT_KEY",
    # Context utilities
    "set_context",
    "get_context",
    "clear_context",
    # Request context
    "get_current_request",
    "get_current_user",
    # Tenant context
    "get_current_tenant",
    "set_current_tenant",
    "get_current_organization",
    "set_current_organization",
    # Tracing
    "set_request_id",
    "get_request_id",
    "set_correlation_id",
    "get_correlation_id",
    # Request metadata
    "get_client_ip",
    "get_user_agent",
)

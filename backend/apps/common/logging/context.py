"""
Logging context utilities.

Provides structured logging context extracted from the current
execution context.

This module is intentionally read-only and never raises errors
during logging operations.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from apps.common.logging.constants import (
    CLIENT_IP_FIELD,
    CORRELATION_ID_FIELD,
    ORGANIZATION_ID_FIELD,
    REQUEST_ID_FIELD,
    TENANT_ID_FIELD,
    TIMESTAMP_FIELD,
    USER_AGENT_FIELD,
    USER_ID_FIELD,
    USERNAME_FIELD,
)


def get_logging_context() -> dict[str, Any]:
    """
    Return structured logging context.

    Logging must never break application execution.
    Missing context values are returned as ``None``.
    """

    try:
        from apps.common.middleware.context import (
            get_client_ip,
            get_context,
            get_correlation_id,
            get_current_user,
            get_request_id,
            get_user_agent,
        )

    except ImportError:
        return {
            TIMESTAMP_FIELD: datetime.now(
                UTC,
            ).isoformat(),
        }

    user = get_current_user()

    tenant = get_context(
        "tenant",
    )

    organization = get_context(
        "organization",
    )

    username = None

    if user:
        username_method = getattr(
            user,
            "get_username",
            None,
        )

        if callable(username_method):
            username = username_method()

    return {
        TIMESTAMP_FIELD: datetime.now(
            UTC,
        ).isoformat(),
        REQUEST_ID_FIELD: get_request_id(),
        CORRELATION_ID_FIELD: get_correlation_id(),
        USER_ID_FIELD: getattr(
            user,
            "pk",
            None,
        ),
        USERNAME_FIELD: username,
        TENANT_ID_FIELD: getattr(
            tenant,
            "pk",
            tenant,
        ),
        ORGANIZATION_ID_FIELD: getattr(
            organization,
            "pk",
            organization,
        ),
        CLIENT_IP_FIELD: get_client_ip(),
        USER_AGENT_FIELD: get_user_agent(),
    }


__all__: tuple[str, ...] = ("get_logging_context",)

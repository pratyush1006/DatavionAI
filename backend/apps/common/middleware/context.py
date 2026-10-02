"""
Request context middleware.

Stores request-scoped context using ASGI-safe local storage.

Provides access to:

- request
- request id
- correlation id
- tenant
- organization

without explicitly passing them through application layers.
"""

from __future__ import annotations

from typing import Any

from asgiref.local import Local
from django.http import (
    HttpRequest,
    HttpResponseBase,
)

from apps.common.middleware.base import (
    BaseMiddleware,
)

_REQUEST_CONTEXT = Local()


REQUEST_CONTEXT_KEY = "request"

REQUEST_ID_CONTEXT_KEY = "request_id"

CORRELATION_ID_CONTEXT_KEY = "correlation_id"

TENANT_CONTEXT_KEY = "tenant"

ORGANIZATION_CONTEXT_KEY = "organization"


_CONTEXT_KEYS = (
    REQUEST_CONTEXT_KEY,
    REQUEST_ID_CONTEXT_KEY,
    CORRELATION_ID_CONTEXT_KEY,
    TENANT_CONTEXT_KEY,
    ORGANIZATION_CONTEXT_KEY,
)


def set_context(
    key: str,
    value: object,
) -> None:
    """
    Store a request-scoped value.
    """

    setattr(
        _REQUEST_CONTEXT,
        key,
        value,
    )


def get_context(
    key: str,
) -> object | None:
    """
    Retrieve a request-scoped value.
    """

    return getattr(
        _REQUEST_CONTEXT,
        key,
        None,
    )


def clear_context() -> None:
    """
    Remove all request context values.
    """

    for key in _CONTEXT_KEYS:
        if hasattr(
            _REQUEST_CONTEXT,
            key,
        ):
            delattr(
                _REQUEST_CONTEXT,
                key,
            )


def get_current_request() -> HttpRequest | None:
    """
    Return current request.
    """

    request = get_context(
        REQUEST_CONTEXT_KEY,
    )

    return (
        request
        if isinstance(
            request,
            HttpRequest,
        )
        else None
    )


def get_current_user() -> Any | None:
    """
    Return authenticated user.
    """

    request = get_current_request()

    if request is None:
        return None

    user = getattr(
        request,
        "user",
        None,
    )

    if not user:
        return None

    if not getattr(
        user,
        "is_authenticated",
        False,
    ):
        return None

    return user


def set_request_id(
    request_id: str,
) -> None:
    """
    Store request ID.
    """

    set_context(
        REQUEST_ID_CONTEXT_KEY,
        request_id,
    )


def get_request_id() -> str | None:
    """
    Return request ID.
    """

    value = get_context(
        REQUEST_ID_CONTEXT_KEY,
    )

    return (
        value
        if isinstance(
            value,
            str,
        )
        else None
    )


def set_correlation_id(
    correlation_id: str,
) -> None:
    """
    Store correlation ID.
    """

    set_context(
        CORRELATION_ID_CONTEXT_KEY,
        correlation_id,
    )


def get_correlation_id() -> str | None:
    """
    Return correlation ID.
    """

    value = get_context(
        CORRELATION_ID_CONTEXT_KEY,
    )

    return (
        value
        if isinstance(
            value,
            str,
        )
        else None
    )


def set_current_tenant(
    tenant: object,
) -> None:
    """
    Store current tenant.
    """

    set_context(
        TENANT_CONTEXT_KEY,
        tenant,
    )


def get_current_tenant() -> object | None:
    """
    Return current tenant.
    """

    return get_context(
        TENANT_CONTEXT_KEY,
    )


def set_current_organization(
    organization: object,
) -> None:
    """
    Store current organization.
    """

    set_context(
        ORGANIZATION_CONTEXT_KEY,
        organization,
    )


def get_current_organization() -> object | None:
    """
    Return current organization.
    """

    return get_context(
        ORGANIZATION_CONTEXT_KEY,
    )


def get_client_ip() -> str | None:
    """
    Return client IP.
    """

    request = get_current_request()

    if request is None:
        return None

    forwarded = request.META.get(
        "HTTP_X_FORWARDED_FOR",
    )

    if forwarded:
        return forwarded.split(
            ",",
            maxsplit=1,
        )[0].strip()

    return request.META.get(
        "REMOTE_ADDR",
    )


def get_user_agent() -> str | None:
    """
    Return user agent.
    """

    request = get_current_request()

    if request is None:
        return None

    return request.META.get(
        "HTTP_USER_AGENT",
    )


class RequestContextMiddleware(
    BaseMiddleware,
):
    """
    Initialize and clear request context.
    """

    def process_request(
        self,
        request: HttpRequest,
    ) -> None:
        """
        Store request.
        """

        set_context(
            REQUEST_CONTEXT_KEY,
            request,
        )

    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        """
        Cleanup request context.
        """

        clear_context()

        return response

    def process_exception(
        self,
        request: HttpRequest,
        exception: Exception,
    ) -> None:
        """
        Cleanup after exception.
        """

        clear_context()

        return


__all__: tuple[str, ...] = (
    "CORRELATION_ID_CONTEXT_KEY",
    "ORGANIZATION_CONTEXT_KEY",
    "REQUEST_CONTEXT_KEY",
    "REQUEST_ID_CONTEXT_KEY",
    "TENANT_CONTEXT_KEY",
    "RequestContextMiddleware",
    "clear_context",
    "get_client_ip",
    "get_context",
    "get_correlation_id",
    "get_current_organization",
    "get_current_request",
    "get_current_tenant",
    "get_current_user",
    "get_request_id",
    "get_user_agent",
    "set_context",
    "set_current_organization",
    "set_current_tenant",
    "set_correlation_id",
    "set_request_id",
)

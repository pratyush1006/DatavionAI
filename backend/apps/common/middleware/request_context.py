"""
Request context middleware.

Stores the current request in request-local storage so it can
be accessed throughout request processing without explicitly
passing it between layers.

Note:
    Client IP resolution using ``X-Forwarded-For`` should only
    be trusted when the application is deployed behind a trusted
    reverse proxy.
"""

from __future__ import annotations

from typing import Any

from asgiref.local import Local
from django.http import (
    HttpRequest,
    HttpResponse,
)

from apps.common.middleware.base import BaseMiddleware

_request_context = Local()


def get_current_request() -> HttpRequest | None:
    """
    Return the current request if available.
    """

    return getattr(
        _request_context,
        "request",
        None,
    )


def get_current_user() -> Any | None:
    """
    Return the authenticated user for the current request.

    Returns:
        The authenticated user, or ``None`` if no authenticated
        user is associated with the current request.
    """

    request = get_current_request()

    if request is None:
        return None

    user = getattr(
        request,
        "user",
        None,
    )

    if user is None or not user.is_authenticated:
        return None

    return user


def get_client_ip() -> str | None:
    """
    Return the client IP address.
    """

    request = get_current_request()

    if request is None:
        return None

    forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR",
    )

    if forwarded_for:
        return forwarded_for.split(
            ",",
        )[0].strip()

    return request.META.get(
        "REMOTE_ADDR",
    )


def get_user_agent() -> str | None:
    """
    Return the current request's user agent.
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
    Store the current request for the lifetime of the request.
    """

    def __call__(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        """
        Store and clean up the current request.
        """

        _request_context.request = request

        try:
            return self.get_response(
                request,
            )

        finally:
            if hasattr(
                _request_context,
                "request",
            ):
                del _request_context.request


__all__ = [
    "RequestContextMiddleware",
    "get_client_ip",
    "get_current_request",
    "get_current_user",
    "get_user_agent",
]

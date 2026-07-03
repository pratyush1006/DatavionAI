"""
Request context middleware.

Stores the current request in request-local storage so it can
be accessed anywhere in the application without explicitly
passing it through every function.
"""

from __future__ import annotations

from typing import Any

from asgiref.local import Local
from django.http import (
    HttpRequest,
    HttpResponse,
)

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

    Returns None if there is no active request or the user
    is not authenticated.
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
        return forwarded_for.split(",")[0].strip()

    return request.META.get(
        "REMOTE_ADDR",
    )


def get_user_agent() -> str | None:
    """
    Return the request user agent.
    """

    request = get_current_request()

    if request is None:
        return None

    return request.META.get(
        "HTTP_USER_AGENT",
    )


class RequestContextMiddleware:
    """
    Middleware storing the current request in request-local storage.
    """

    def __init__(
        self,
        get_response,
    ) -> None:
        self.get_response = get_response

    def __call__(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        """
        Store the current request for the duration of the request lifecycle.
        """

        _request_context.request = request

        try:
            response = self.get_response(
                request,
            )
        finally:
            if hasattr(
                _request_context,
                "request",
            ):
                del _request_context.request

        return response


__all__ = [
    "RequestContextMiddleware",
    "get_client_ip",
    "get_current_request",
    "get_current_user",
    "get_user_agent",
]

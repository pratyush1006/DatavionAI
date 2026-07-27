"""
HTTP request utilities.

Provides reusable helpers for incoming HTTP requests.
"""

from __future__ import annotations

from django.http import HttpRequest

from apps.common.http.models import (
    ClientContext,
    GeoLocation,
)
from apps.common.http.types import (
    Headers,
)


def get_client_ip(
    request: HttpRequest,
) -> str:
    """
    Return the originating client IP address.
    """

    forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR",
    )

    if forwarded_for:
        return forwarded_for.split(
            ",",
            maxsplit=1,
        )[0].strip()

    return request.META.get(
        "REMOTE_ADDR",
        "",
    )


def get_client_user_agent(
    request: HttpRequest,
) -> str:
    """
    Return the client's User-Agent.
    """

    return request.META.get(
        "HTTP_USER_AGENT",
        "",
    )


def get_client_device(
    request: HttpRequest,
) -> str:
    """
    Return the client device identifier from User-Agent.
    """

    return get_client_user_agent(
        request,
    )


def get_client_host(
    request: HttpRequest,
) -> str:
    """
    Return the request host.
    """

    return request.get_host()


def get_request_method(
    request: HttpRequest,
) -> str:
    """
    Return the HTTP method.
    """

    return request.method


def get_request_path(
    request: HttpRequest,
) -> str:
    """
    Return the request path.
    """

    return request.path


def get_request_scheme(
    request: HttpRequest,
) -> str:
    """
    Return the request scheme.
    """

    return request.scheme


def is_secure_request(
    request: HttpRequest,
) -> bool:
    """
    Return whether the request uses HTTPS.
    """

    return request.is_secure()


def get_request_headers(
    request: HttpRequest,
) -> Headers:
    """
    Return normalized request headers.
    """

    return {key: value for key, value in request.headers.items()}


def get_client_location(
    request: HttpRequest,
) -> GeoLocation:
    """
    Return the client's geolocation.

    The default implementation performs no GeoIP lookup.
    """

    del request

    return GeoLocation()


def get_client_context(
    request: HttpRequest,
) -> ClientContext:
    """
    Build the immutable client context.
    """

    return ClientContext(
        ip_address=get_client_ip(request),
        user_agent=get_client_user_agent(request),
        host=get_client_host(request),
        scheme=get_request_scheme(request),
        method=get_request_method(request),
        path=get_request_path(request),
        query_string=request.META.get(
            "QUERY_STRING",
            "",
        ),
        headers=get_request_headers(request),
        is_secure=is_secure_request(request),
        location=get_client_location(request),
    )


__all__: tuple[str, ...] = (
    "get_client_context",
    "get_client_device",
    "get_client_host",
    "get_client_ip",
    "get_client_location",
    "get_client_user_agent",
    "get_request_headers",
    "get_request_method",
    "get_request_path",
    "get_request_scheme",
    "is_secure_request",
)

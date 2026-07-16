"""
HTTP client helper utilities.
"""

from __future__ import annotations

from rest_framework.request import Request


def get_client_ip(
    request: Request,
) -> str:
    """
    Return the client's IP address.

    Supports reverse proxies by preferring
    X-Forwarded-For when available.
    """

    forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR",
    )

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get(
        "REMOTE_ADDR",
        "",
    )


def get_client_user_agent(
    request: Request,
) -> str:
    """
    Return the client's User-Agent header.
    """

    return request.META.get(
        "HTTP_USER_AGENT",
        "Unknown Device",
    )


def get_client_device(
    request: Request,
) -> str:
    """
    Return the client device.

    Currently returns the User-Agent string.

    Future versions will parse browser,
    operating system and device type.
    """

    return get_client_user_agent(
        request,
    )


def get_client_location(
    request: Request,
) -> str:
    """
    Return the client's location.

    Placeholder until GeoIP support is added.
    """

    return "Unknown Location"


__all__ = [
    "get_client_device",
    "get_client_ip",
    "get_client_location",
    "get_client_user_agent",
]

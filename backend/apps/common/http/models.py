"""
HTTP models.

Provides immutable models shared across the DatavionAI
HTTP framework.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.http.types import Headers


@dataclass(
    frozen=True,
    slots=True,
)
class GeoLocation:
    """
    Client geolocation information.
    """

    country: str | None = None

    country_code: str | None = None

    region: str | None = None

    city: str | None = None

    postal_code: str | None = None

    latitude: float | None = None

    longitude: float | None = None

    timezone: str | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class ClientContext:
    """
    Immutable client request context.
    """

    ip_address: str

    user_agent: str

    host: str

    scheme: str

    method: str

    path: str

    query_string: str

    headers: Headers

    is_secure: bool

    location: GeoLocation


__all__: tuple[str, ...] = (
    "ClientContext",
    "GeoLocation",
)

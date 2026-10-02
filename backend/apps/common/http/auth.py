"""
HTTP authentication strategies.

Provides reusable authentication strategies for the DatavionAI
HTTP framework.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Protocol

from apps.common.http.types import Headers


class AuthenticationStrategy(
    Protocol,
):
    """
    Protocol for HTTP authentication strategies.
    """

    def apply(
        self,
        headers: Headers,
    ) -> Headers:
        """
        Apply authentication to the supplied headers.
        """


@dataclass(
    frozen=True,
    slots=True,
)
class NoAuthentication:
    """
    No authentication.
    """

    def apply(
        self,
        headers: Headers,
    ) -> Headers:
        return dict(headers)


@dataclass(
    frozen=True,
    slots=True,
)
class BearerTokenAuthentication:
    """
    Bearer token authentication.
    """

    token: str

    def apply(
        self,
        headers: Headers,
    ) -> Headers:
        updated = dict(headers)

        updated["Authorization"] = f"Bearer {self.token}"

        return updated


@dataclass(
    frozen=True,
    slots=True,
)
class APIKeyAuthentication:
    """
    API key authentication.
    """

    api_key: str

    header_name: str = "X-API-Key"

    def apply(
        self,
        headers: Headers,
    ) -> Headers:
        updated = dict(headers)

        updated[self.header_name] = self.api_key

        return updated


@dataclass(
    frozen=True,
    slots=True,
)
class BasicAuthentication:
    """
    HTTP Basic authentication.
    """

    username: str

    password: str

    def apply(
        self,
        headers: Headers,
    ) -> Headers:
        credentials = (f"{self.username}:{self.password}").encode()

        encoded = base64.b64encode(
            credentials,
        ).decode(
            "ascii",
        )

        updated = dict(headers)

        updated["Authorization"] = f"Basic {encoded}"

        return updated


__all__: tuple[str, ...] = (
    "APIKeyAuthentication",
    "AuthenticationStrategy",
    "BasicAuthentication",
    "BearerTokenAuthentication",
    "NoAuthentication",
)

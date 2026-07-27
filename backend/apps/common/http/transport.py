"""
HTTP transport abstractions.

Defines the transport interface used by the DatavionAI
HTTP framework.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import Literal

from apps.common.http.config import (
    RequestOptions,
)
from apps.common.http.response import (
    HTTPResponse,
)
from apps.common.http.types import (
    ResponseData,
)

HTTPMethod = Literal[
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "HEAD",
    "OPTIONS",
]


class HTTPTransport(
    ABC,
):
    """
    Base HTTP transport.
    """

    @abstractmethod
    def request(
        self,
        *,
        method: HTTPMethod,
        url: str,
        options: RequestOptions,
        json: ResponseData | None = None,
        content: bytes | None = None,
    ) -> HTTPResponse:
        """
        Execute an HTTP request.
        """

    @abstractmethod
    def close(
        self,
    ) -> None:
        """
        Release transport resources.
        """


__all__: tuple[str, ...] = (
    "HTTPMethod",
    "HTTPTransport",
)

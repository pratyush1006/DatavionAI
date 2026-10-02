"""
HTTP response models.

Provides immutable response models shared across the
DatavionAI HTTP framework.
"""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from apps.common.http.types import (
    Headers,
    ResponseData,
)


@dataclass(
    frozen=True,
    slots=True,
)
class HTTPResponse:
    """
    Generic HTTP response.
    """

    status_code: int

    headers: Headers

    data: ResponseData | None = None

    content: bytes = b""

    encoding: str = "utf-8"

    @property
    def status(
        self,
    ) -> HTTPStatus | None:
        """
        Return the HTTP status enumeration.
        """

        try:
            return HTTPStatus(
                self.status_code,
            )

        except ValueError:
            return None

    @property
    def is_success(
        self,
    ) -> bool:
        """
        Return whether the response is successful.
        """

        return 200 <= self.status_code < 300

    @property
    def is_redirect(
        self,
    ) -> bool:
        """
        Return whether the response is a redirect.
        """

        return 300 <= self.status_code < 400

    @property
    def is_client_error(
        self,
    ) -> bool:
        """
        Return whether the response is a client error.
        """

        return 400 <= self.status_code < 500

    @property
    def is_server_error(
        self,
    ) -> bool:
        """
        Return whether the response is a server error.
        """

        return 500 <= self.status_code < 600

    @property
    def is_error(
        self,
    ) -> bool:
        """
        Return whether the response represents an error.
        """

        return self.status_code >= 400


@dataclass(
    frozen=True,
    slots=True,
)
class JSONResponse(
    HTTPResponse,
):
    """
    JSON HTTP response.
    """

    data: ResponseData


@dataclass(
    frozen=True,
    slots=True,
)
class EmptyResponse(
    HTTPResponse,
):
    """
    Empty HTTP response.
    """

    data: None = None

    content: bytes = b""


def is_success_response(
    response: HTTPResponse,
) -> bool:
    """
    Return whether a response is successful.
    """

    return response.is_success


def is_redirect_response(
    response: HTTPResponse,
) -> bool:
    """
    Return whether a response is a redirect.
    """

    return response.is_redirect


def is_client_error_response(
    response: HTTPResponse,
) -> bool:
    """
    Return whether a response is a client error.
    """

    return response.is_client_error


def is_server_error_response(
    response: HTTPResponse,
) -> bool:
    """
    Return whether a response is a server error.
    """

    return response.is_server_error


def is_error_response(
    response: HTTPResponse,
) -> bool:
    """
    Return whether a response is an error.
    """

    return response.is_error


__all__: tuple[str, ...] = (
    "EmptyResponse",
    "HTTPResponse",
    "JSONResponse",
    "is_client_error_response",
    "is_error_response",
    "is_redirect_response",
    "is_server_error_response",
    "is_success_response",
)

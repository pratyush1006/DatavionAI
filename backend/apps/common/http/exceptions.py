"""
HTTP exception hierarchy.

Provides reusable exceptions for the DatavionAI HTTP framework.
"""

from __future__ import annotations

from http import HTTPStatus


class HTTPClientError(Exception):
    """
    Base exception for all HTTP client errors.
    """


class HTTPRequestError(HTTPClientError):
    """
    Raised when an HTTP request cannot be completed.
    """


class HTTPConnectionError(HTTPRequestError):
    """
    Raised when a connection cannot be established.
    """


class HTTPTimeoutError(HTTPRequestError):
    """
    Raised when an HTTP request exceeds the configured timeout.
    """


class HTTPResponseError(HTTPClientError):
    """
    Raised when an HTTP response indicates an error.
    """

    def __init__(
        self,
        *,
        status_code: int,
        message: str,
    ) -> None:
        """
        Initialize the exception.

        Args:
            status_code:
                HTTP response status code.

            message:
                Human-readable error message.
        """

        super().__init__(
            message,
        )

        self.status_code = status_code

        self.message = message

    @property
    def status(
        self,
    ) -> HTTPStatus | None:
        """
        Return the response status as an HTTPStatus when possible.
        """

        try:
            return HTTPStatus(
                self.status_code,
            )

        except ValueError:
            return None


class HTTPAuthenticationError(HTTPResponseError):
    """
    Raised for HTTP 401 responses.
    """


class HTTPAuthorizationError(HTTPResponseError):
    """
    Raised for HTTP 403 responses.
    """


class HTTPNotFoundError(HTTPResponseError):
    """
    Raised for HTTP 404 responses.
    """


class HTTPServerError(HTTPResponseError):
    """
    Raised for HTTP 5xx responses.
    """


__all__: tuple[str, ...] = (
    "HTTPAuthenticationError",
    "HTTPAuthorizationError",
    "HTTPClientError",
    "HTTPConnectionError",
    "HTTPNotFoundError",
    "HTTPRequestError",
    "HTTPResponseError",
    "HTTPServerError",
    "HTTPTimeoutError",
)

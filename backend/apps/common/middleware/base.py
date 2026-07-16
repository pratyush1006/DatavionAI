"""
Base middleware implementations for the Datavion AI platform.
"""

from __future__ import annotations

from collections.abc import Callable

from django.http import (
    HttpRequest,
    HttpResponse,
)


class BaseMiddleware:
    """
    Base class for Datavion middleware.

    Subclasses should override ``__call__`` when request processing
    is required.
    """

    def __init__(
        self,
        get_response: Callable[
            [HttpRequest],
            HttpResponse,
        ],
    ) -> None:
        """
        Initialize the middleware.
        """

        self.get_response = get_response

    def __call__(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        """
        Process the incoming request.

        Subclasses may override this method to implement custom
        request/response behavior.
        """

        return self.get_response(
            request,
        )


__all__ = [
    "BaseMiddleware",
]

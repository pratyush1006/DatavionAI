"""
Base middleware implementations for the DatavionAI framework.
"""

from __future__ import annotations

from collections.abc import Callable

from django.http import (
    HttpRequest,
    HttpResponseBase,
)

MiddlewareHandler = Callable[
    [HttpRequest],
    HttpResponseBase,
]


class BaseMiddleware:
    """
    Base class for DatavionAI middleware.

    Subclasses should override lifecycle hooks instead of
    implementing ``__call__`` directly.
    """

    def __init__(
        self,
        get_response: MiddlewareHandler,
    ) -> None:
        """
        Initialize middleware.
        """

        self.get_response = get_response

    def process_request(
        self,
        request: HttpRequest,
    ) -> None:
        """
        Process incoming request.

        Executed before the view.
        """

    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        """
        Process outgoing response.
        """

        return response

    def process_exception(
        self,
        request: HttpRequest,
        exception: Exception,
    ) -> HttpResponseBase | None:
        """
        Process request exceptions.

        Returning a response prevents exception propagation.
        """

        return None

    def __call__(
        self,
        request: HttpRequest,
    ) -> HttpResponseBase:
        """
        Execute middleware lifecycle.
        """

        self.process_request(
            request,
        )

        try:
            response = self.get_response(
                request,
            )

        except Exception as exception:
            handled_response = self.process_exception(
                request,
                exception,
            )

            if handled_response is not None:
                return handled_response

            raise

        return self.process_response(
            request,
            response,
        )


__all__: tuple[str, ...] = ("BaseMiddleware",)

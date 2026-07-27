"""
Correlation ID middleware.

Provides distributed request correlation for the DatavionAI
platform.

Correlation IDs allow tracing across:

- API requests
- background jobs
- external integrations
- asynchronous workflows
"""

from __future__ import annotations

from uuid import (
    UUID,
    uuid4,
)

from django.http import (
    HttpRequest,
    HttpResponseBase,
)

from apps.common.middleware.base import (
    BaseMiddleware,
)
from apps.common.middleware.context import (
    clear_context,
    get_correlation_id,
    set_correlation_id,
)

CORRELATION_ID_HEADER = "X-Correlation-ID"

MAX_CORRELATION_ID_LENGTH = 64


def _is_valid_correlation_id(
    value: str,
) -> bool:
    """
    Validate incoming correlation ID.
    """

    if not value:
        return False

    if len(value) > MAX_CORRELATION_ID_LENGTH:
        return False

    try:
        UUID(value)

    except ValueError:
        return False

    return True


class CorrelationIDMiddleware(
    BaseMiddleware,
):
    """
    Assign correlation ID to every request.

    Incoming correlation IDs are reused only when valid.
    """

    def process_request(
        self,
        request: HttpRequest,
    ) -> None:
        """
        Create or reuse correlation ID.
        """

        incoming_id = request.headers.get(
            CORRELATION_ID_HEADER,
        )

        correlation_id = (
            incoming_id
            if incoming_id
            and _is_valid_correlation_id(
                incoming_id,
            )
            else str(
                uuid4(),
            )
        )

        request.correlation_id = correlation_id

        set_correlation_id(
            correlation_id,
        )

    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        """
        Add correlation ID response header.
        """

        correlation_id = get_correlation_id()

        if correlation_id:
            response[CORRELATION_ID_HEADER] = correlation_id

        clear_context()

        return response

    def process_exception(
        self,
        request: HttpRequest,
        exception: Exception,
    ) -> None:
        """
        Clear request context after failures.
        """

        clear_context()

        return


__all__: tuple[str, ...] = (
    "CORRELATION_ID_HEADER",
    "CorrelationIDMiddleware",
)

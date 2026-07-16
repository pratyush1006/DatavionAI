"""
Logging configuration utilities.

Provides reusable logging components shared across the
Datavion AI platform.
"""

from __future__ import annotations

import logging

from apps.common.middleware import get_request_id

DEFAULT_REQUEST_ID = "-"


class RequestIDFilter(
    logging.Filter,
):
    """
    Inject the current request ID into every log record.
    """

    def filter(
        self,
        record: logging.LogRecord,
    ) -> bool:
        """
        Add the current request ID to the log record.
        """

        record.request_id = get_request_id() or DEFAULT_REQUEST_ID

        return True


__all__ = [
    "RequestIDFilter",
]

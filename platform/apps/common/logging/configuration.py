"""
Logging configuration utilities.

Provides reusable logging components shared across the
Datavion AI platform.
"""

from __future__ import annotations

from logging import (
    Filter,
    LogRecord,
)

from apps.common.middleware import get_request_id


class RequestIDFilter(Filter):
    """
    Inject the current request ID into every log record.
    """

    def filter(
        self,
        record: LogRecord,
    ) -> bool:
        """
        Add the current request ID to the log record.
        """

        record.request_id = get_request_id() or "-"

        return True


__all__ = [
    "RequestIDFilter",
]

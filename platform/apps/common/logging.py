"""
Logging utilities.

Provides logging helpers shared across the Datavion platform.
"""

from __future__ import annotations

from logging import (
    Filter,
    LogRecord,
)

from apps.common.request_id import get_request_id


class RequestIDFilter(Filter):
    """
    Inject the current request ID into every log record.
    """

    def filter(
        self,
        record: LogRecord,
    ) -> bool:
        record.request_id = get_request_id() or "-"
        return True


__all__ = [
    "RequestIDFilter",
]

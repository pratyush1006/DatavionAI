"""
Logging utilities.
"""

from apps.common.request_id import get_request_id


class RequestIDFilter:
    """
    Inject the current request ID into every log record.
    """

    def filter(self, record):
        record.request_id = get_request_id() or "-"
        return True

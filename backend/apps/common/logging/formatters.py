"""
Logging formatters.

Provides structured logging formatters for the DatavionAI
observability framework.
"""

from __future__ import annotations

import json
import logging
from datetime import (
    UTC,
    datetime,
)
from typing import Any

from apps.common.logging.constants import (
    APPLICATION_FIELD,
    CLIENT_IP_FIELD,
    CORRELATION_ID_FIELD,
    ENVIRONMENT_FIELD,
    EVENT_CATEGORY_FIELD,
    EVENT_NAME_FIELD,
    EVENT_TYPE_FIELD,
    EXCEPTION_FIELD,
    FUNCTION_FIELD,
    LEVEL_FIELD,
    LOGGER_FIELD,
    MESSAGE_FIELD,
    MODULE_FIELD,
    ORGANIZATION_ID_FIELD,
    REQUEST_ID_FIELD,
    REQUEST_METHOD_FIELD,
    REQUEST_PATH_FIELD,
    SPAN_ID_FIELD,
    STACK_TRACE_FIELD,
    STATUS_CODE_FIELD,
    TENANT_ID_FIELD,
    TIMESTAMP_FIELD,
    TRACE_ID_FIELD,
    USER_AGENT_FIELD,
    USER_ID_FIELD,
    USERNAME_FIELD,
    VERSION_FIELD,
)


class JSONFormatter(
    logging.Formatter,
):
    """
    Format log records as structured JSON.
    """

    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        """
        Format a log record as JSON.
        """

        log: dict[str, Any] = {
            TIMESTAMP_FIELD: datetime.now(
                UTC,
            ).isoformat(),
            LEVEL_FIELD: record.levelname,
            LOGGER_FIELD: record.name,
            MESSAGE_FIELD: record.getMessage(),
            MODULE_FIELD: record.module,
            FUNCTION_FIELD: record.funcName,
            REQUEST_ID_FIELD: getattr(
                record,
                REQUEST_ID_FIELD,
                None,
            ),
            CORRELATION_ID_FIELD: getattr(
                record,
                CORRELATION_ID_FIELD,
                None,
            ),
            TRACE_ID_FIELD: getattr(
                record,
                TRACE_ID_FIELD,
                None,
            ),
            SPAN_ID_FIELD: getattr(
                record,
                SPAN_ID_FIELD,
                None,
            ),
            USER_ID_FIELD: getattr(
                record,
                USER_ID_FIELD,
                None,
            ),
            USERNAME_FIELD: getattr(
                record,
                USERNAME_FIELD,
                None,
            ),
            TENANT_ID_FIELD: getattr(
                record,
                TENANT_ID_FIELD,
                None,
            ),
            ORGANIZATION_ID_FIELD: getattr(
                record,
                ORGANIZATION_ID_FIELD,
                None,
            ),
            CLIENT_IP_FIELD: getattr(
                record,
                CLIENT_IP_FIELD,
                None,
            ),
            USER_AGENT_FIELD: getattr(
                record,
                USER_AGENT_FIELD,
                None,
            ),
            REQUEST_METHOD_FIELD: getattr(
                record,
                REQUEST_METHOD_FIELD,
                None,
            ),
            REQUEST_PATH_FIELD: getattr(
                record,
                REQUEST_PATH_FIELD,
                None,
            ),
            STATUS_CODE_FIELD: getattr(
                record,
                STATUS_CODE_FIELD,
                None,
            ),
            APPLICATION_FIELD: getattr(
                record,
                APPLICATION_FIELD,
                None,
            ),
            ENVIRONMENT_FIELD: getattr(
                record,
                ENVIRONMENT_FIELD,
                None,
            ),
            VERSION_FIELD: getattr(
                record,
                VERSION_FIELD,
                None,
            ),
            EVENT_TYPE_FIELD: getattr(
                record,
                EVENT_TYPE_FIELD,
                None,
            ),
            EVENT_NAME_FIELD: getattr(
                record,
                EVENT_NAME_FIELD,
                None,
            ),
            EVENT_CATEGORY_FIELD: getattr(
                record,
                EVENT_CATEGORY_FIELD,
                None,
            ),
        }

        if record.exc_info:
            exception = self.formatException(
                record.exc_info,
            )

            log[EXCEPTION_FIELD] = exception

            log[STACK_TRACE_FIELD] = exception

        return json.dumps(
            log,
            ensure_ascii=False,
            default=str,
        )


class ConsoleFormatter(
    logging.Formatter,
):
    """
    Human-readable formatter for development.
    """

    default_format = "[%(levelname)s] %(asctime)s %(name)s %(message)s"

    default_date_format = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self,
    ) -> None:
        """
        Initialize formatter.
        """

        super().__init__(
            fmt=self.default_format,
            datefmt=self.default_date_format,
        )

    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        """
        Format log output safely.

        Prevents logging failures caused by
        mutated messages with original args.
        """

        try:
            request_id = getattr(
                record,
                REQUEST_ID_FIELD,
                None,
            )

            if request_id:
                record_copy = logging.makeLogRecord(
                    record.__dict__.copy(),
                )

                record_copy.msg = f"[{request_id}] {record.getMessage()}"

                # Important:
                # clear original formatting args
                record_copy.args = ()

                return super().format(
                    record_copy,
                )

            return super().format(
                record,
            )

        except Exception:
            return f"[{record.levelname}] {record.name} {record.msg}"


__all__: tuple[str, ...] = (
    "ConsoleFormatter",
    "JSONFormatter",
)

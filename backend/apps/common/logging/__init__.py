"""
Public logging API for DatavionAI.

Provides the stable public interface for the framework logging
package. Applications should import logging helpers from this
package instead of implementation modules.
"""

from __future__ import annotations

from .audit import (
    AUDIT_LOGGER_NAME,
    DEFAULT_AUDIT_MESSAGE,
    get_audit_logger,
    log_audit_event,
)
from .constants import (
    APPLICATION_FIELD,
    CLIENT_IP_FIELD,
    CORRELATION_ID_FIELD,
    DEFAULT_LOGGER_NAME,
    ENVIRONMENT_FIELD,
    EVENT_CATEGORY_FIELD,
    EVENT_NAME_FIELD,
    EVENT_TYPE_FIELD,
    EXCEPTION_FIELD,
    EXCEPTION_TYPE_FIELD,
    FUNCTION_FIELD,
    LEVEL_FIELD,
    LINE_NUMBER_FIELD,
    LOGGER_FIELD,
    MESSAGE_FIELD,
    MODULE_FIELD,
    ORGANIZATION_ID_FIELD,
    PROCESS_ID_FIELD,
    REQUEST_ID_FIELD,
    REQUEST_METHOD_FIELD,
    REQUEST_PATH_FIELD,
    SPAN_ID_FIELD,
    STACK_TRACE_FIELD,
    STATUS_CODE_FIELD,
    TENANT_ID_FIELD,
    THREAD_ID_FIELD,
    TIMESTAMP_FIELD,
    TRACE_ID_FIELD,
    USER_AGENT_FIELD,
    USER_ID_FIELD,
    USERNAME_FIELD,
    VERSION_FIELD,
)
from .context import (
    get_logging_context,
)
from .filters import (
    HealthCheckFilter,
    RequestContextFilter,
    SensitiveDataFilter,
)
from .formatters import (
    ConsoleFormatter,
    JSONFormatter,
)
from .handlers import (
    create_console_handler,
    create_json_console_handler,
    create_rotating_file_handler,
)
from .logger import (
    configure_logger,
    get_logger,
)

__all__: tuple[str, ...] = (
    # Audit
    "AUDIT_LOGGER_NAME",
    "DEFAULT_AUDIT_MESSAGE",
    "get_audit_logger",
    "log_audit_event",
    # Constants
    "APPLICATION_FIELD",
    "CLIENT_IP_FIELD",
    "CORRELATION_ID_FIELD",
    "DEFAULT_LOGGER_NAME",
    "ENVIRONMENT_FIELD",
    "EVENT_CATEGORY_FIELD",
    "EVENT_NAME_FIELD",
    "EVENT_TYPE_FIELD",
    "EXCEPTION_FIELD",
    "EXCEPTION_TYPE_FIELD",
    "FUNCTION_FIELD",
    "LEVEL_FIELD",
    "LINE_NUMBER_FIELD",
    "LOGGER_FIELD",
    "MESSAGE_FIELD",
    "MODULE_FIELD",
    "ORGANIZATION_ID_FIELD",
    "PROCESS_ID_FIELD",
    "REQUEST_ID_FIELD",
    "REQUEST_METHOD_FIELD",
    "REQUEST_PATH_FIELD",
    "SPAN_ID_FIELD",
    "STACK_TRACE_FIELD",
    "STATUS_CODE_FIELD",
    "TENANT_ID_FIELD",
    "THREAD_ID_FIELD",
    "TIMESTAMP_FIELD",
    "TRACE_ID_FIELD",
    "USER_AGENT_FIELD",
    "USER_ID_FIELD",
    "USERNAME_FIELD",
    "VERSION_FIELD",
    # Context
    "get_logging_context",
    # Filters
    "HealthCheckFilter",
    "RequestContextFilter",
    "SensitiveDataFilter",
    # Formatters
    "ConsoleFormatter",
    "JSONFormatter",
    # Handlers
    "create_console_handler",
    "create_json_console_handler",
    "create_rotating_file_handler",
    # Logger
    "configure_logger",
    "get_logger",
)

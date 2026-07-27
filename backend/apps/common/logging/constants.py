"""
Logging constants.

Defines framework-wide constants used throughout the DatavionAI
logging infrastructure.
"""

from __future__ import annotations

DEFAULT_LOGGER_NAME = "datavion"


# Request Context

REQUEST_ID_FIELD = "request_id"

CORRELATION_ID_FIELD = "correlation_id"

TRACE_ID_FIELD = "trace_id"

SPAN_ID_FIELD = "span_id"


# Identity Context

USER_ID_FIELD = "user_id"

USERNAME_FIELD = "username"

ORGANIZATION_ID_FIELD = "organization_id"

TENANT_ID_FIELD = "tenant_id"


# Client Context

CLIENT_IP_FIELD = "client_ip"

USER_AGENT_FIELD = "user_agent"


# HTTP Context

REQUEST_METHOD_FIELD = "request_method"

REQUEST_PATH_FIELD = "request_path"

STATUS_CODE_FIELD = "status_code"


# Event Context

EVENT_TYPE_FIELD = "event_type"

EVENT_NAME_FIELD = "event_name"

EVENT_CATEGORY_FIELD = "event_category"


# Exception Context

EXCEPTION_FIELD = "exception"

EXCEPTION_TYPE_FIELD = "exception_type"

STACK_TRACE_FIELD = "stack_trace"


# Application Context

APPLICATION_FIELD = "application"

ENVIRONMENT_FIELD = "environment"

VERSION_FIELD = "version"


# Log Metadata

TIMESTAMP_FIELD = "timestamp"

LOGGER_FIELD = "logger"

LEVEL_FIELD = "level"

MESSAGE_FIELD = "message"

MODULE_FIELD = "module"

FUNCTION_FIELD = "function"

LINE_NUMBER_FIELD = "line"

PROCESS_ID_FIELD = "process"

THREAD_ID_FIELD = "thread"


__all__: tuple[str, ...] = (
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
)

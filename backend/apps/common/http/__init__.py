"""
DatavionAI HTTP framework.

Provides reusable HTTP abstractions, client utilities,
configuration, authentication strategies, request helpers,
response models, transport abstractions, and exception types.
"""

from __future__ import annotations

from apps.common.http.auth import (
    APIKeyAuthentication,
    AuthenticationStrategy,
    BasicAuthentication,
    BearerTokenAuthentication,
    NoAuthentication,
)
from apps.common.http.client import (
    HTTPClient,
)
from apps.common.http.config import (
    DEFAULT_CLIENT_CONFIGURATION,
    DEFAULT_REQUEST_OPTIONS,
    ClientConfiguration,
    RequestOptions,
)
from apps.common.http.exceptions import (
    HTTPAuthenticationError,
    HTTPAuthorizationError,
    HTTPClientError,
    HTTPConnectionError,
    HTTPNotFoundError,
    HTTPRequestError,
    HTTPResponseError,
    HTTPServerError,
    HTTPTimeoutError,
)
from apps.common.http.models import (
    ClientContext,
    GeoLocation,
)
from apps.common.http.request import (
    get_client_context,
    get_client_device,
    get_client_host,
    get_client_ip,
    get_client_location,
    get_client_user_agent,
    get_request_headers,
    get_request_method,
    get_request_path,
    get_request_scheme,
    is_secure_request,
)
from apps.common.http.response import (
    EmptyResponse,
    HTTPResponse,
    JSONResponse,
)
from apps.common.http.retry import (
    DEFAULT_RETRY_CONFIGURATION,
    RetryConfiguration,
)
from apps.common.http.status import (
    Status,
    StatusCode,
    is_client_error,
    is_error,
    is_informational,
    is_redirect,
    is_server_error,
    is_success,
)
from apps.common.http.timeout import (
    DEFAULT_TIMEOUT_CONFIGURATION,
    TimeoutConfiguration,
)
from apps.common.http.transport import (
    HTTPMethod,
    HTTPTransport,
)

__all__: tuple[str, ...] = (
    # Client
    "HTTPClient",
    # Configuration
    "ClientConfiguration",
    "DEFAULT_CLIENT_CONFIGURATION",
    "DEFAULT_REQUEST_OPTIONS",
    "RequestOptions",
    # Authentication
    "APIKeyAuthentication",
    "AuthenticationStrategy",
    "BasicAuthentication",
    "BearerTokenAuthentication",
    "NoAuthentication",
    # Models
    "ClientContext",
    "GeoLocation",
    # Request Helpers
    "get_client_context",
    "get_client_device",
    "get_client_host",
    "get_client_ip",
    "get_client_location",
    "get_client_user_agent",
    "get_request_headers",
    "get_request_method",
    "get_request_path",
    "get_request_scheme",
    "is_secure_request",
    # Response Models
    "EmptyResponse",
    "HTTPResponse",
    "JSONResponse",
    # Retry
    "DEFAULT_RETRY_CONFIGURATION",
    "RetryConfiguration",
    # Timeout
    "DEFAULT_TIMEOUT_CONFIGURATION",
    "TimeoutConfiguration",
    # Status
    "Status",
    "StatusCode",
    "is_client_error",
    "is_error",
    "is_informational",
    "is_redirect",
    "is_server_error",
    "is_success",
    # Transport
    "HTTPMethod",
    "HTTPTransport",
    # Exceptions
    "HTTPAuthenticationError",
    "HTTPAuthorizationError",
    "HTTPClientError",
    "HTTPConnectionError",
    "HTTPNotFoundError",
    "HTTPRequestError",
    "HTTPResponseError",
    "HTTPServerError",
    "HTTPTimeoutError",
)

"""
DatavionAI API Metrics Constants.

Centralized metrics and observability constants used throughout the
DatavionAI platform.

This module defines metric namespaces, metric types, labels,
monitoring systems, and telemetry identifiers.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No Prometheus implementation
- No business logic
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Metric Namespace
###############################################################################

METRIC_NAMESPACE: Final[str] = "datavion"

METRIC_SUBSYSTEM_API: Final[str] = "api"

METRIC_SUBSYSTEM_DATABASE: Final[str] = "database"

METRIC_SUBSYSTEM_CACHE: Final[str] = "cache"

METRIC_SUBSYSTEM_QUEUE: Final[str] = "queue"

METRIC_SUBSYSTEM_STORAGE: Final[str] = "storage"

METRIC_SUBSYSTEM_AUTH: Final[str] = "authentication"

###############################################################################
# Metric Types
###############################################################################


class MetricType(StrEnum):
    """
    Supported metric types.
    """

    COUNTER = "counter"

    GAUGE = "gauge"

    HISTOGRAM = "histogram"

    SUMMARY = "summary"


SUPPORTED_METRIC_TYPES: Final[tuple[str, ...]] = (
    MetricType.COUNTER.value,
    MetricType.GAUGE.value,
    MetricType.HISTOGRAM.value,
    MetricType.SUMMARY.value,
)

###############################################################################
# Common Metric Labels
###############################################################################

LABEL_METHOD: Final[str] = "method"

LABEL_ENDPOINT: Final[str] = "endpoint"

LABEL_ROUTE: Final[str] = "route"

LABEL_STATUS: Final[str] = "status"

LABEL_STATUS_CODE: Final[str] = "status_code"

LABEL_SERVICE: Final[str] = "service"

LABEL_INSTANCE: Final[str] = "instance"

LABEL_VERSION: Final[str] = "version"

LABEL_ENVIRONMENT: Final[str] = "environment"

LABEL_TENANT: Final[str] = "tenant"

###############################################################################
# Telemetry Providers
###############################################################################

PROVIDER_PROMETHEUS: Final[str] = "prometheus"

PROVIDER_OPENTELEMETRY: Final[str] = "opentelemetry"

PROVIDER_DATADOG: Final[str] = "datadog"

PROVIDER_GRAFANA: Final[str] = "grafana"

PROVIDER_NEW_RELIC: Final[str] = "newrelic"

PROVIDER_ELASTIC: Final[str] = "elastic"

SUPPORTED_PROVIDERS: Final[tuple[str, ...]] = (
    PROVIDER_PROMETHEUS,
    PROVIDER_OPENTELEMETRY,
    PROVIDER_DATADOG,
    PROVIDER_GRAFANA,
    PROVIDER_NEW_RELIC,
    PROVIDER_ELASTIC,
)

###############################################################################
# Standard Metric Names
###############################################################################

METRIC_HTTP_REQUESTS: Final[str] = "http_requests_total"

METRIC_HTTP_DURATION: Final[str] = "http_request_duration_seconds"

METRIC_HTTP_EXCEPTIONS: Final[str] = "http_exceptions_total"

METRIC_DATABASE_QUERIES: Final[str] = "database_queries_total"

METRIC_CACHE_HITS: Final[str] = "cache_hits_total"

METRIC_CACHE_MISSES: Final[str] = "cache_misses_total"

METRIC_QUEUE_JOBS: Final[str] = "queue_jobs_total"

METRIC_STORAGE_OPERATIONS: Final[str] = "storage_operations_total"

###############################################################################
# Trace Attributes
###############################################################################

TRACE_SERVICE_NAME: Final[str] = "service.name"

TRACE_SERVICE_VERSION: Final[str] = "service.version"

TRACE_DEPLOYMENT_ENVIRONMENT: Final[str] = "deployment.environment"

TRACE_HTTP_METHOD: Final[str] = "http.method"

TRACE_HTTP_ROUTE: Final[str] = "http.route"

TRACE_HTTP_STATUS_CODE: Final[str] = "http.status_code"

TRACE_HTTP_TARGET: Final[str] = "http.target"

###############################################################################
# Reserved Labels
###############################################################################

RESERVED_METRIC_LABELS: Final[frozenset[str]] = frozenset(
    {
        LABEL_METHOD,
        LABEL_ENDPOINT,
        LABEL_ROUTE,
        LABEL_STATUS,
        LABEL_STATUS_CODE,
        LABEL_SERVICE,
        LABEL_INSTANCE,
        LABEL_VERSION,
        LABEL_ENVIRONMENT,
        LABEL_TENANT,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "MetricType",
)

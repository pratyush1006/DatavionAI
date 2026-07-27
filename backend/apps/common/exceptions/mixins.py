"""
DatavionAI Exception Mixins.

Reusable mixins for enterprise exception handling.

Design Principles
-----------------
- Framework agnostic
- Composable
- Immutable by convention
- Serialization friendly
"""

from __future__ import annotations

from typing import Any


class DetailMixin:
    """
    Adds structured detail payload.
    """

    detail: Any = None

    def set_detail(
        self,
        detail: Any,
    ) -> None:
        self.detail = detail


class FieldErrorsMixin:
    """
    Adds field-level validation errors.
    """

    field_errors: dict[str, list[str]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.field_errors = {}
        super().__init__(*args, **kwargs)

    def add_field_error(
        self,
        field: str,
        message: str,
    ) -> None:
        self.field_errors.setdefault(
            field,
            [],
        ).append(message)


class ResourceMixin:
    """
    Adds resource metadata.
    """

    resource: str | None = None
    identifier: str | int | None = None

    def set_resource(
        self,
        resource: str,
        identifier: str | int | None = None,
    ) -> None:
        self.resource = resource
        self.identifier = identifier


class RetryMixin:
    """
    Adds retry metadata.
    """

    retryable: bool = False
    retry_after: int | None = None

    def enable_retry(
        self,
        retry_after: int | None = None,
    ) -> None:
        self.retryable = True
        self.retry_after = retry_after


class CorrelationMixin:
    """
    Adds request tracing metadata.
    """

    request_id: str | None = None
    correlation_id: str | None = None
    trace_id: str | None = None

    def set_trace(
        self,
        *,
        request_id: str | None = None,
        correlation_id: str | None = None,
        trace_id: str | None = None,
    ) -> None:
        self.request_id = request_id
        self.correlation_id = correlation_id
        self.trace_id = trace_id


class MetadataMixin:
    """
    Adds arbitrary metadata.
    """

    metadata: dict[str, Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.metadata = {}
        super().__init__(*args, **kwargs)

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        self.metadata[key] = value


__all__ = (
    "CorrelationMixin",
    "DetailMixin",
    "FieldErrorsMixin",
    "MetadataMixin",
    "ResourceMixin",
    "RetryMixin",
)

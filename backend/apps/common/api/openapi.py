"""
Reusable OpenAPI utilities for Datavion APIs.

This module provides a centralized import location for
drf-spectacular utilities used across the platform.

Feature applications should import these utilities from
this module instead of importing directly from
drf-spectacular.
"""

from __future__ import annotations

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)

__all__ = [
    "OpenApiExample",
    "OpenApiParameter",
    "OpenApiResponse",
    "OpenApiTypes",
    "extend_schema",
    "extend_schema_view",
]

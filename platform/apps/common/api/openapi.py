"""
Reusable OpenAPI utilities for Datavion APIs.

This module centralizes reusable OpenAPI helpers based on
drf-spectacular. Feature applications should import these
utilities instead of importing directly from drf-spectacular.
"""

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

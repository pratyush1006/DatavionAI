"""
Reusable OpenAPI utilities for the DatavionOS framework.

Provides the framework-owned OpenAPI abstraction layer.

Supports:

- Schema decorators
- Common parameters
- API examples
- Standard response documentation
- Multi-tenant API documentation

Feature applications should import from this module
instead of importing drf-spectacular directly.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import (
    OpenApiExample as DatavionOpenApiExample,
)
from drf_spectacular.utils import (
    OpenApiParameter as DatavionOpenApiParameter,
)
from drf_spectacular.utils import (
    OpenApiResponse as DatavionOpenApiResponse,
)
from drf_spectacular.utils import (
    OpenApiTypes as DatavionOpenApiTypes,
)
from drf_spectacular.utils import (
    extend_schema as datavion_extend_schema,
)
from drf_spectacular.utils import (
    extend_schema_view as datavion_extend_schema_view,
)

# ============================================================================
# Backward compatible aliases
# ============================================================================

extend_schema = datavion_extend_schema
extend_schema_view = datavion_extend_schema_view

# ============================================================================
# Common API Parameters
# ============================================================================

DATAVION_REQUEST_ID_PARAMETER: Final = DatavionOpenApiParameter(
    name="X-Request-ID",
    type=DatavionOpenApiTypes.STR,
    location=DatavionOpenApiParameter.HEADER,
    required=False,
    description="Unique request correlation identifier.",
)

DATAVION_TENANT_PARAMETER: Final = DatavionOpenApiParameter(
    name="X-Tenant-ID",
    type=DatavionOpenApiTypes.UUID,
    location=DatavionOpenApiParameter.HEADER,
    required=False,
    description="Current tenant identifier.",
)

DATAVION_ORGANIZATION_PARAMETER: Final = DatavionOpenApiParameter(
    name="X-Organization-ID",
    type=DatavionOpenApiTypes.UUID,
    location=DatavionOpenApiParameter.HEADER,
    required=False,
    description="Current organization identifier.",
)

# ============================================================================
# Standard API Examples
# ============================================================================

DATAVION_SUCCESS_EXAMPLE: Final = DatavionOpenApiExample(
    "Success Response",
    value={
        "success": True,
        "message": "Success.",
        "data": {},
        "meta": {},
    },
)

DATAVION_ERROR_EXAMPLE: Final = DatavionOpenApiExample(
    "Error Response",
    value={
        "success": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Validation failed.",
        },
        "meta": {},
    },
)

# ============================================================================
# API Tags
# ============================================================================

DATAVION_API_TAGS: Final[tuple[str, ...]] = (
    "Authentication",
    "Organizations",
    "Users",
    "Patients",
    "Clinical",
    "Laboratory",
    "Appointments",
    "Documents",
    "Workflow",
    "AI",
    "Search",
    "Reports",
    "Billing",
)

# ============================================================================
# Public Exports
# ============================================================================

__all__: Final[tuple[str, ...]] = (
    # DRF Spectacular wrappers
    "DatavionOpenApiExample",
    "DatavionOpenApiParameter",
    "DatavionOpenApiResponse",
    "DatavionOpenApiTypes",
    # Decorators
    "datavion_extend_schema",
    "datavion_extend_schema_view",
    # Backward compatibility
    "extend_schema",
    "extend_schema_view",
    # Parameters
    "DATAVION_REQUEST_ID_PARAMETER",
    "DATAVION_TENANT_PARAMETER",
    "DATAVION_ORGANIZATION_PARAMETER",
    # Examples
    "DATAVION_SUCCESS_EXAMPLE",
    "DATAVION_ERROR_EXAMPLE",
    # Tags
    "DATAVION_API_TAGS",
)

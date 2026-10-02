"""
Backward-compatible import for request ID middleware.

The canonical implementation lives in:
apps.common.middleware.request_id
"""

from __future__ import annotations

from apps.common.middleware.request_id import (
    REQUEST_ID_HEADER,
    RequestIDMiddleware,
)

__all__: tuple[str, ...] = (
    "REQUEST_ID_HEADER",
    "RequestIDMiddleware",
)

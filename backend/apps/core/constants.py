"""
Core application constants.
"""

from __future__ import annotations

# ---------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------

APP_NAME = "Datavion AI"

APP_VERSION = "1.0.0"

# ---------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------

HEALTHY = "healthy"
UNHEALTHY = "unhealthy"

ALIVE = "alive"

READY = "ready"
NOT_READY = "not_ready"

__all__ = [
    "ALIVE",
    "APP_NAME",
    "APP_VERSION",
    "HEALTHY",
    "NOT_READY",
    "READY",
    "UNHEALTHY",
]

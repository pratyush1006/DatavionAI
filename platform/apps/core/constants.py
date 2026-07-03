"""
Core application constants.
"""

from __future__ import annotations

APP_NAME = "Datavion AI"

APP_VERSION = "1.0.0"

# Health status
HEALTHY = "healthy"
UNHEALTHY = "unhealthy"

# Liveness probe
ALIVE = "alive"

# Readiness probe
READY = "ready"
NOT_READY = "not_ready"


__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "HEALTHY",
    "UNHEALTHY",
    "ALIVE",
    "READY",
    "NOT_READY",
]

"""
Platform lifecycle signals for the Datavion AI platform.
"""

from __future__ import annotations

from .application import (
    application_started,
    application_stopping,
)

__all__ = [
    "application_started",
    "application_stopping",
]

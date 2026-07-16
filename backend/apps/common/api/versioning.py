"""
Reusable API versioning classes.

This module provides a centralized import location for the
versioning strategies used across the Datavion AI platform.

Datavion currently uses DRF's default versioning strategies.
Custom versioning implementations should only be introduced
when a genuine cross-cutting requirement exists.
"""

from __future__ import annotations

from rest_framework.versioning import (
    NamespaceVersioning,
    URLPathVersioning,
)

__all__ = [
    "NamespaceVersioning",
    "URLPathVersioning",
]

"""
Reusable API versioning classes for the DatavionAI framework.

This module provides the framework-owned import surface for API
versioning strategies used throughout the platform.

DatavionAI currently relies on Django REST Framework's built-in
versioning strategies. Feature applications should import
versioning classes from this module rather than directly from DRF.

Custom versioning implementations should only be introduced when a
genuine cross-cutting framework requirement exists.
"""

from __future__ import annotations

from rest_framework.versioning import (
    NamespaceVersioning as DatavionNamespaceVersioning,
)
from rest_framework.versioning import (
    URLPathVersioning as DatavionURLPathVersioning,
)

__all__: tuple[str, ...] = (
    "DatavionNamespaceVersioning",
    "DatavionURLPathVersioning",
)

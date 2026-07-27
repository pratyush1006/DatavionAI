"""
Platform system checks.

Importing this package registers all Django system checks.
"""

from __future__ import annotations

from . import ai, cache, celery, database, email, redis, security, storage

__all__ = [
    "ai",
    "cache",
    "celery",
    "database",
    "email",
    "redis",
    "security",
    "storage",
]

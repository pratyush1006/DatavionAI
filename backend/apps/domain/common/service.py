"""
Domain service contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)


@runtime_checkable
class DomainService(
    Protocol,
):
    """
    Marker protocol for domain services.

    Domain services encapsulate business logic that does not
    naturally belong to a single entity or aggregate.
    """

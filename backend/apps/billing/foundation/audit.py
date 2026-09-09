"""Billing audit actor primitive."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AuditActor:
    """Identify the user and organization responsible for an operation."""

    user_id: Any
    organization_id: Any


__all__ = ["AuditActor"]

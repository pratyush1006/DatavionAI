from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class OrganizationControlPlaneSnapshot:
    """Read model for the active organization administration workspace."""

    organization: dict[str, Any]
    subscription: dict[str, Any] | None
    modules: list[dict[str, Any]]
    features: list[dict[str, Any]]
    can_manage_modules: bool
    can_manage_features: bool

"""
Security service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.security.authentication import (
    AuthenticationService,
)
from apps.datavionos.security.authorization import (
    AuthorizationService,
)
from apps.datavionos.security.evaluator import (
    AuthorizationEvaluator,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityServices:
    """
    Aggregate of security services.
    """

    authentication: AuthenticationService

    authorization: AuthorizationService

    evaluator: AuthorizationEvaluator


__all__ = [
    "SecurityServices",
]

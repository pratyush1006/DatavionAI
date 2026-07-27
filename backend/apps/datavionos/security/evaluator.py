"""
Authorization evaluator contracts.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from apps.datavionos.security.authorization import (
    AuthorizationRequest,
    AuthorizationResult,
)
from apps.datavionos.security.context import (
    SecurityContext,
)


@runtime_checkable
class AuthorizationEvaluator(
    Protocol,
):
    """
    Evaluates authorization requests against
    the current security context.
    """

    async def evaluate(
        self,
        context: SecurityContext,
        request: AuthorizationRequest,
    ) -> AuthorizationResult:
        """
        Evaluate an authorization request.
        """


__all__ = [
    "AuthorizationEvaluator",
]

"""
Audit middleware.
"""

from __future__ import annotations


class AuditMiddleware:
    """
    Audit middleware.

    The DatavionAI platform already provides request context
    through RequestContextMiddleware. This middleware is kept as
    an extension point for future audit-specific functionality
    such as correlation IDs, distributed tracing, or external
    audit integrations.
    """

    def __init__(
        self,
        get_response,
    ):
        self.get_response = get_response

    def __call__(
        self,
        request,
    ):
        """
        Process the incoming request.
        """

        return self.get_response(
            request,
        )


__all__ = [
    "AuditMiddleware",
]

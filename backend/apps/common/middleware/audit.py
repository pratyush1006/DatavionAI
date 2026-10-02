"""
Audit middleware.

Collects request metadata for audit logging.

This middleware does not persist audit records.
It prepares request-scoped audit context consumed by:

- audit services
- structured logging
- security monitoring
- compliance reporting
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from django.http import (
    HttpRequest,
    HttpResponseBase,
)

from apps.common.middleware.base import (
    BaseMiddleware,
)
from apps.common.middleware.context import (
    get_client_ip,
    get_correlation_id,
    get_current_organization,
    get_current_tenant,
    get_current_user,
    get_request_id,
    get_user_agent,
)


class AuditMiddleware(
    BaseMiddleware,
):
    """
    Populate request audit metadata.
    """

    def process_request(
        self,
        request: HttpRequest,
    ) -> None:
        """
        Collect audit request information.
        """

        user = get_current_user()

        tenant = get_current_tenant()

        organization = get_current_organization()

        request._audit_start_time = perf_counter()

        request.audit = {
            "request_id": get_request_id(),
            "correlation_id": get_correlation_id(),
            "user_id": getattr(
                user,
                "pk",
                None,
            ),
            "tenant_id": getattr(
                tenant,
                "pk",
                tenant,
            ),
            "organization_id": getattr(
                organization,
                "pk",
                organization,
            ),
            "client_ip": get_client_ip(),
            "user_agent": get_user_agent(),
            "method": request.method,
            "path": request.path,
        }

    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        """
        Add response audit metadata.
        """

        audit: dict[str, Any] = getattr(
            request,
            "audit",
            {},
        )

        started = getattr(
            request,
            "_audit_start_time",
            None,
        )

        duration_ms = None

        if started is not None:
            duration_ms = round(
                (perf_counter() - started) * 1000,
                2,
            )

        audit.update(
            {
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "success": response.status_code < 400,
            }
        )

        request.audit = audit

        return response

    def process_exception(
        self,
        request: HttpRequest,
        exception: Exception,
    ) -> None:
        """
        Mark failed requests.
        """

        audit: dict[str, Any] = getattr(
            request,
            "audit",
            {},
        )

        audit.update(
            {
                "success": False,
                "exception": exception.__class__.__name__,
            }
        )

        request.audit = audit

        return


__all__: tuple[str, ...] = ("AuditMiddleware",)

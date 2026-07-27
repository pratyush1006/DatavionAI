"""
Audit middleware.

Captures request lifecycle information for DatavionOS audit tracking.
"""

from __future__ import annotations

import time

from apps.platform.audit.constants import (
    AuditAction,
)
from apps.platform.audit.services import (
    AuditService,
)


class AuditMiddleware:
    """
    Audit request lifecycle middleware.

    Responsibilities:

    - Capture request execution metadata
    - Capture failed requests
    - Preserve request correlation
    - Create system audit records

    Request IDs are provided by RequestIDMiddleware.
    Tenant context is provided by TenantMiddleware.
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

        start_time = time.time()

        response = None

        try:
            response = self.get_response(
                request,
            )

            return response

        except Exception as exc:
            self._log_request_failure(
                request=request,
                exception=exc,
            )

            raise

        finally:
            if response is not None:
                self._log_request_completion(
                    request=request,
                    response=response,
                    duration=(time.time() - start_time),
                )

    def _log_request_completion(
        self,
        *,
        request,
        response,
        duration: float,
    ):
        """
        Record completed request.

        Avoid noisy audit creation for static assets.
        """

        if self._ignore_path(
            request.path,
        ):
            return

        if request.method in {
            "GET",
            "HEAD",
            "OPTIONS",
        }:
            return

        AuditService.log_event(
            action=(AuditAction.UPDATE),
            module="system",
            object_type="HTTP_REQUEST",
            object_id=request.path,
            success=(response.status_code < 400),
            status_code=response.status_code,
            new_values={
                "method": request.method,
                "duration_ms": round(
                    duration * 1000,
                    2,
                ),
            },
        )

    def _log_request_failure(
        self,
        *,
        request,
        exception,
    ):
        """
        Record failed request.
        """

        if self._ignore_path(
            request.path,
        ):
            return

        AuditService.log_event(
            action=AuditAction.UPDATE,
            module="system",
            object_type="HTTP_REQUEST",
            object_id=request.path,
            success=False,
            error_message=str(
                exception,
            ),
        )

    def _ignore_path(
        self,
        path: str,
    ) -> bool:
        """
        Ignore non-business requests.
        """

        ignored = (
            "/static/",
            "/media/",
            "/favicon.ico",
            "/health/",
        )

        return path.startswith(
            ignored,
        )


__all__ = [
    "AuditMiddleware",
]

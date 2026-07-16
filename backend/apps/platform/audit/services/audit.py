"""
Business services for the Audit application.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.common.middleware.request_context import (
    get_client_ip,
    get_current_request,
    get_current_user,
    get_user_agent,
)
from apps.platform.audit.constants import AuditAction
from apps.platform.audit.models import AuditLog


class AuditService:
    """
    Business services for audit logging.
    """

    @staticmethod
    @transaction.atomic
    def log_event(
        *,
        action: AuditAction,
        module: str,
        object_type: str,
        object_id: str,
        organization=None,
        user=None,
        old_values: dict[str, Any] | None = None,
        new_values: dict[str, Any] | None = None,
        success: bool = True,
        error_message: str = "",
        status_code: int | None = None,
    ) -> AuditLog:
        """
        Create an immutable audit log entry.
        """

        request = get_current_request()

        return AuditLog.objects.create(
            organization=organization,
            user=user or get_current_user(),
            action=action,
            module=module,
            object_type=object_type,
            object_id=object_id,
            old_values=old_values,
            new_values=new_values,
            request_id=(
                getattr(
                    request,
                    "request_id",
                    "",
                )
                if request
                else ""
            ),
            correlation_id=(
                getattr(
                    request,
                    "correlation_id",
                    "",
                )
                if request
                else ""
            ),
            session_key=(
                request.session.session_key
                if (request and hasattr(request, "session"))
                else ""
            ),
            ip_address=get_client_ip(),
            user_agent=get_user_agent() or "",
            http_method=(request.method if request else ""),
            request_path=(request.path if request else ""),
            status_code=status_code,
            success=success,
            error_message=error_message,
        )

    @classmethod
    def log_create(
        cls,
        **kwargs,
    ) -> AuditLog:
        """
        Log object creation.
        """

        return cls.log_event(
            action=AuditAction.CREATE,
            **kwargs,
        )

    @classmethod
    def log_update(
        cls,
        **kwargs,
    ) -> AuditLog:
        """
        Log object update.
        """

        return cls.log_event(
            action=AuditAction.UPDATE,
            **kwargs,
        )

    @classmethod
    def log_delete(
        cls,
        **kwargs,
    ) -> AuditLog:
        """
        Log object deletion.
        """

        return cls.log_event(
            action=AuditAction.DELETE,
            **kwargs,
        )

    @classmethod
    def log_restore(
        cls,
        **kwargs,
    ) -> AuditLog:
        """
        Log object restoration.
        """

        return cls.log_event(
            action=AuditAction.RESTORE,
            **kwargs,
        )

    @classmethod
    def log_login(
        cls,
        **kwargs,
    ) -> AuditLog:
        """
        Log user login.
        """

        return cls.log_event(
            action=AuditAction.LOGIN,
            **kwargs,
        )

    @classmethod
    def log_logout(
        cls,
        **kwargs,
    ) -> AuditLog:
        """
        Log user logout.
        """

        return cls.log_event(
            action=AuditAction.LOGOUT,
            **kwargs,
        )


__all__ = [
    "AuditService",
]

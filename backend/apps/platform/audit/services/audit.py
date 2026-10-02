"""
Business services for the Audit application.

Central audit service for DatavionOS.

Responsibilities:

- Create immutable audit records
- Resolve tenant context
- Capture request metadata
- Support healthcare PHI auditing
- Support security auditing
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.common.middleware.context import (
    get_client_ip,
    get_current_request,
    get_current_user,
    get_user_agent,
)
from apps.platform.audit.constants import (
    AuditAction,
)
from apps.platform.audit.models import (
    AuditLog,
)
from apps.platform.tenancy.context import (
    get_tenant_context,
)


class AuditService:
    """
    Enterprise audit logging service.
    """

    @staticmethod
    def _resolve_context():
        """
        Resolve current tenant context.
        """

        return get_tenant_context()

    @staticmethod
    @transaction.atomic
    def log_event(
        *,
        action: AuditAction,
        module: str,
        object_type: str,
        object_id: str,
        tenant=None,
        organization=None,
        user=None,
        old_values: dict[str, Any] | None = None,
        new_values: dict[str, Any] | None = None,
        success: bool = True,
        error_message: str = "",
        status_code: int | None = None,
    ) -> AuditLog:
        """
        Create immutable audit entry.
        """

        request = get_current_request()

        context = AuditService._resolve_context()

        if context:
            tenant = tenant or context.tenant

            organization = organization or getattr(
                context,
                "organization",
                None,
            )

            user = user or context.user

        return AuditLog.objects.create(
            tenant=tenant,
            organization=organization,
            user=(user or get_current_user()),
            action=action,
            module=module,
            object_type=object_type,
            object_id=str(
                object_id,
            ),
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
                if (
                    request
                    and hasattr(
                        request,
                        "session",
                    )
                )
                else ""
            ),
            ip_address=get_client_ip(),
            user_agent=(get_user_agent() or ""),
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
    ):
        return cls.log_event(
            action=AuditAction.CREATE,
            **kwargs,
        )

    @classmethod
    def log_update(
        cls,
        **kwargs,
    ):
        return cls.log_event(
            action=AuditAction.UPDATE,
            **kwargs,
        )

    @classmethod
    def log_delete(
        cls,
        **kwargs,
    ):
        return cls.log_event(
            action=AuditAction.DELETE,
            **kwargs,
        )

    @classmethod
    def log_restore(
        cls,
        **kwargs,
    ):
        return cls.log_event(
            action=AuditAction.RESTORE,
            **kwargs,
        )

    @classmethod
    def log_login(
        cls,
        **kwargs,
    ):
        return cls.log_event(
            action=AuditAction.LOGIN,
            **kwargs,
        )

    @classmethod
    def log_logout(
        cls,
        **kwargs,
    ):
        return cls.log_event(
            action=AuditAction.LOGOUT,
            **kwargs,
        )

    # ================================================================
    # Healthcare / PHI Audit Helpers
    # ================================================================

    @classmethod
    def log_phi_access(
        cls,
        *,
        module: str,
        object_type: str,
        object_id: str,
        **kwargs,
    ):
        """
        Record PHI access event.

        Example:
            Doctor viewed patient record.
        """

        return cls.log_event(
            action=AuditAction.VIEW,
            module=module,
            object_type=object_type,
            object_id=object_id,
            **kwargs,
        )

    @classmethod
    def log_export(
        cls,
        **kwargs,
    ):
        """
        Record data export.
        """

        return cls.log_event(
            action=AuditAction.EXPORT,
            **kwargs,
        )

    @classmethod
    def log_permission_change(
        cls,
        **kwargs,
    ):
        """
        Record RBAC permission changes.
        """

        return cls.log_event(
            action=AuditAction.PERMISSION_CHANGE,
            module="rbac",
            **kwargs,
        )

    @classmethod
    def log_role_change(
        cls,
        **kwargs,
    ):
        """
        Record role assignment changes.
        """

        return cls.log_event(
            action=AuditAction.ROLE_CHANGE,
            module="rbac",
            **kwargs,
        )

    # ================================================================
    # AI Governance Audit Helpers
    # ================================================================

    @classmethod
    def log_ai_event(
        cls,
        *,
        action: AuditAction,
        object_type: str,
        object_id: str,
        old_values: dict[str, Any] | None = None,
        new_values: dict[str, Any] | None = None,
        **kwargs,
    ):
        """
        Record AI governance events.

        Examples:

        - AI response generated
        - AI recommendation approved
        - AI feedback submitted
        """

        return cls.log_event(
            action=action,
            module="ai",
            object_type=object_type,
            object_id=object_id,
            old_values=old_values,
            new_values=new_values,
            **kwargs,
        )

    # ================================================================
    # Workflow Audit Helpers
    # ================================================================

    @classmethod
    def log_workflow_event(
        cls,
        *,
        action: AuditAction,
        object_type: str,
        object_id: str,
        old_values: dict[str, Any] | None = None,
        new_values: dict[str, Any] | None = None,
        **kwargs,
    ):
        """
        Record workflow lifecycle events.

        Examples:

        - workflow started
        - workflow approved
        - workflow rejected
        """

        return cls.log_event(
            action=action,
            module="workflow",
            object_type=object_type,
            object_id=object_id,
            old_values=old_values,
            new_values=new_values,
            **kwargs,
        )

    # ================================================================
    # Security Audit Helpers
    # ================================================================

    @classmethod
    def log_failed_login(
        cls,
        **kwargs,
    ):
        """
        Record failed authentication attempt.
        """

        return cls.log_event(
            action=AuditAction.FAILED_LOGIN,
            module="accounts",
            object_type="Authentication",
            **kwargs,
        )

    @classmethod
    def log_password_reset(
        cls,
        **kwargs,
    ):
        """
        Record password reset event.
        """

        return cls.log_event(
            action=AuditAction.PASSWORD_RESET,
            module="accounts",
            object_type="PasswordReset",
            **kwargs,
        )


__all__ = [
    "AuditService",
]

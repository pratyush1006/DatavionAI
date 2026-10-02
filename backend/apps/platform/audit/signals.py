"""
Platform-wide audit signal handlers.

Handles infrastructure-level audit events:

- Authentication
- Security events
- RBAC changes

Domain modules should call AuditService directly
for business events.
"""

from __future__ import annotations

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

from apps.platform.audit.constants import (
    AuditAction,
)
from apps.platform.audit.services import (
    AuditService,
)

# ============================================================================
# Authentication Events
# ============================================================================


@receiver(
    user_logged_in,
)
def audit_user_login(
    sender,
    request,
    user,
    **kwargs,
):
    """
    Audit successful login.
    """

    AuditService.log_event(
        action=AuditAction.LOGIN,
        module="accounts",
        object_type="User",
        object_id=str(
            user.id,
        ),
        user=user,
        success=True,
    )


@receiver(
    user_logged_out,
)
def audit_user_logout(
    sender,
    request,
    user,
    **kwargs,
):
    """
    Audit logout.
    """

    if user is None:
        return

    AuditService.log_event(
        action=AuditAction.LOGOUT,
        module="accounts",
        object_type="User",
        object_id=str(
            user.id,
        ),
        user=user,
        success=True,
    )


@receiver(
    user_login_failed,
)
def audit_failed_login(
    sender,
    credentials,
    request,
    **kwargs,
):
    """
    Audit failed login attempts.
    """

    AuditService.log_event(
        action=AuditAction.FAILED_LOGIN,
        module="accounts",
        object_type="Authentication",
        object_id="LOGIN_ATTEMPT",
        success=False,
        error_message=("Authentication failed"),
    )


__all__ = [
    "audit_user_login",
    "audit_user_logout",
    "audit_failed_login",
]

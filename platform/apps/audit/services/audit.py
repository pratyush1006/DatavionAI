"""
Business services for the Audit application.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.audit.constants import (
    AUDIT_ACTION_CREATE,
    AUDIT_ACTION_DELETE,
    AUDIT_ACTION_LOGIN,
    AUDIT_ACTION_LOGOUT,
    AUDIT_ACTION_RESTORE,
    AUDIT_ACTION_UPDATE,
)
from apps.audit.models import AuditLog
from apps.common.middleware.request_context import (
    get_request_context,
)


@transaction.atomic
def log_event(
    *,
    action: str,
    module: str,
    object_type: str,
    object_id: str,
    organization=None,
    user=None,
    old_values: dict[str, Any] | None = None,
    new_values: dict[str, Any] | None = None,
) -> AuditLog:
    """
    Create an immutable audit log entry.
    """

    context = get_request_context()

    return AuditLog.objects.create(
        organization=organization,
        user=user or context.user,
        action=action,
        module=module,
        object_type=object_type,
        object_id=object_id,
        old_values=old_values,
        new_values=new_values,
        request_id=context.request_id,
        ip_address=context.ip_address,
        user_agent=context.user_agent,
    )


def log_create(
    **kwargs,
) -> AuditLog:
    """
    Log object creation.
    """

    return log_event(
        action=AUDIT_ACTION_CREATE,
        **kwargs,
    )


def log_update(
    **kwargs,
) -> AuditLog:
    """
    Log object update.
    """

    return log_event(
        action=AUDIT_ACTION_UPDATE,
        **kwargs,
    )


def log_delete(
    **kwargs,
) -> AuditLog:
    """
    Log object deletion.
    """

    return log_event(
        action=AUDIT_ACTION_DELETE,
        **kwargs,
    )


def log_restore(
    **kwargs,
) -> AuditLog:
    """
    Log object restoration.
    """

    return log_event(
        action=AUDIT_ACTION_RESTORE,
        **kwargs,
    )


def log_login(
    **kwargs,
) -> AuditLog:
    """
    Log user login.
    """

    return log_event(
        action=AUDIT_ACTION_LOGIN,
        **kwargs,
    )


def log_logout(
    **kwargs,
) -> AuditLog:
    """
    Log user logout.
    """

    return log_event(
        action=AUDIT_ACTION_LOGOUT,
        **kwargs,
    )

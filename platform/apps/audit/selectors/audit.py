"""
Read-only selectors for the Audit application.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.audit.models import AuditLog

type AuditLogQuerySet = QuerySet[AuditLog]

AUDIT_LIST_FIELDS = (
    "id",
    "created_at",
    "action",
    "module",
    "object_type",
    "object_id",
    "user",
    "organization",
)


def get_audit_logs() -> AuditLogQuerySet:
    """
    Return all audit logs ordered by newest first.
    """

    return (
        AuditLog.objects.select_related(
            "user",
            "organization",
        )
        .only(
            *AUDIT_LIST_FIELDS,
        )
        .order_by(
            "-created_at",
        )
    )


def get_audit_log_by_id(
    audit_log_id,
) -> AuditLog:
    """
    Return a single audit log by its primary key.
    """

    return get_object_or_404(
        get_audit_logs(),
        pk=audit_log_id,
    )


def get_user_history(
    *,
    user_id,
) -> AuditLogQuerySet:
    """
    Return audit history for a specific user.
    """

    return get_audit_logs().filter(
        user_id=user_id,
    )


def get_object_history(
    *,
    object_type: str,
    object_id: str,
) -> AuditLogQuerySet:
    """
    Return audit history for a specific object.
    """

    return get_audit_logs().filter(
        object_type=object_type,
        object_id=object_id,
    )


def get_module_history(
    *,
    module: str,
) -> AuditLogQuerySet:
    """
    Return audit history for a module.
    """

    return get_audit_logs().filter(
        module=module,
    )

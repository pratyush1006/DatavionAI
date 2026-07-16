"""
Read-only selectors for the Audit application.
"""

from __future__ import annotations

from datetime import datetime

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.audit.models import AuditLog

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
    "success",
)


def get_audit_logs() -> AuditLogQuerySet:
    """
    Return all audit logs.
    """

    return (
        AuditLog.objects.active()
        .select_related(
            "user",
            "organization",
        )
        .only(
            *AUDIT_LIST_FIELDS,
        )
        .recent()
    )


def get_audit_log_by_id(
    audit_log_id,
) -> AuditLog:
    """
    Return a single audit log.
    """

    return get_object_or_404(
        get_audit_logs(),
        pk=audit_log_id,
    )


def get_organization_history(
    *,
    organization,
) -> AuditLogQuerySet:
    """
    Return audit history for an organization.
    """

    return get_audit_logs().for_organization(
        organization,
    )


def get_user_history(
    *,
    user,
) -> AuditLogQuerySet:
    """
    Return audit history for a user.
    """

    return get_audit_logs().for_user(
        user,
    )


def get_module_history(
    *,
    module: str,
) -> AuditLogQuerySet:
    """
    Return audit history for a module.
    """

    return get_audit_logs().for_module(
        module,
    )


def get_action_history(
    *,
    action: str,
) -> AuditLogQuerySet:
    """
    Return audit history for an action.
    """

    return get_audit_logs().for_action(
        action,
    )


def get_object_history(
    *,
    object_type: str,
    object_id: str,
) -> AuditLogQuerySet:
    """
    Return audit history for an object.
    """

    return get_audit_logs().for_object(
        object_type=object_type,
        object_id=object_id,
    )


def get_audit_logs_between(
    *,
    start: datetime,
    end: datetime,
) -> AuditLogQuerySet:
    """
    Return audit logs within a date range.
    """

    return get_audit_logs().between(
        start=start,
        end=end,
    )


def search_audit_logs(
    *,
    query: str,
) -> AuditLogQuerySet:
    """
    Search audit logs.
    """

    return get_audit_logs().search(
        query,
    )


__all__ = [
    "get_audit_logs",
    "get_audit_log_by_id",
    "get_organization_history",
    "get_user_history",
    "get_module_history",
    "get_action_history",
    "get_object_history",
    "get_audit_logs_between",
    "search_audit_logs",
]

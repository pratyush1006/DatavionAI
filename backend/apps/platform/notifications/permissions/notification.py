"""
Notification permissions.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanAccessNotification(
    BasePermission,
):
    """
    Permission to access notifications.
    """

    message = "You do not have permission to access this notification."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.is_authenticated


class CanRetryNotification(
    BasePermission,
):
    """
    Permission to retry notifications.
    """

    message = "You do not have permission to retry notifications."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.is_authenticated


class CanCancelNotification(
    BasePermission,
):
    """
    Permission to cancel notifications.
    """

    message = "You do not have permission to cancel notifications."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.is_authenticated


class CanMarkNotificationRead(
    BasePermission,
):
    """
    Permission to mark notifications as read.
    """

    message = "You do not have permission to modify notifications."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.is_authenticated


__all__ = [
    "CanAccessNotification",
    "CanCancelNotification",
    "CanMarkNotificationRead",
    "CanRetryNotification",
]

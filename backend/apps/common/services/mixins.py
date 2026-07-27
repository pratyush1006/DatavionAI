"""
DatavionAI Service Mixins.

Reusable mixins for enterprise service classes.

Design Principles
-----------------
- Framework agnostic
- Composable
- Single responsibility
- Lightweight
"""

from __future__ import annotations

from typing import Any

from .permissions import PermissionService
from .transaction import TransactionService
from .validation import ValidationService


class ValidationMixin:
    """
    Validation helpers.
    """

    require = staticmethod(
        ValidationService.require,
    )

    require_not_none = staticmethod(
        ValidationService.require_not_none,
    )

    require_not_empty = staticmethod(
        ValidationService.require_not_empty,
    )

    require_resource = staticmethod(
        ValidationService.require_resource,
    )


class PermissionMixin:
    """
    Permission helpers.
    """

    require_permission = staticmethod(
        PermissionService.require_permission,
    )

    require_authenticated = staticmethod(
        PermissionService.require_authenticated,
    )

    require_active = staticmethod(
        PermissionService.require_active,
    )

    require_staff = staticmethod(
        PermissionService.require_staff,
    )

    require_superuser = staticmethod(
        PermissionService.require_superuser,
    )

    require_any_permission = staticmethod(
        PermissionService.require_any_permission,
    )

    require_all_permissions = staticmethod(
        PermissionService.require_all_permissions,
    )


class TransactionMixin:
    """
    Transaction helpers.
    """

    atomic = staticmethod(
        TransactionService.atomic,
    )

    on_commit = staticmethod(
        TransactionService.on_commit,
    )

    savepoint = staticmethod(
        TransactionService.savepoint,
    )

    savepoint_commit = staticmethod(
        TransactionService.savepoint_commit,
    )

    savepoint_rollback = staticmethod(
        TransactionService.savepoint_rollback,
    )


class ContextMixin:
    """
    Service context helpers.
    """

    user: Any | None = None

    organization: Any | None = None

    request: Any | None = None

    @property
    def is_authenticated(
        self,
    ) -> bool:
        """
        Return True if a user is authenticated.
        """

        return bool(
            self.user
            and getattr(
                self.user,
                "is_authenticated",
                False,
            )
        )


class AuditMixin:
    """
    Audit hook.

    Intended to be overridden by subclasses.
    """

    def audit(
        self,
        *_: Any,
        **__: Any,
    ) -> None:
        """
        Record an audit event.

        Override in subclasses.
        """

        return


class LoggingMixin:
    """
    Logging hook.

    Intended to be overridden by subclasses.
    """

    def log(
        self,
        *_: Any,
        **__: Any,
    ) -> None:
        """
        Log service activity.

        Override in subclasses.
        """

        return


__all__ = (
    "AuditMixin",
    "ContextMixin",
    "LoggingMixin",
    "PermissionMixin",
    "TransactionMixin",
    "ValidationMixin",
)

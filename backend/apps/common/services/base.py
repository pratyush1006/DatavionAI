"""
DatavionAI Base Service.

Enterprise base service for all application services.

Design Principles
-----------------
- Framework agnostic
- Stateless
- Transaction ready
- Validation friendly
- Permission aware
"""

from __future__ import annotations

from typing import Any

from django.db import transaction


class BaseService:
    """
    Base service for all business services.
    """

    def __init__(
        self,
        *,
        user: Any | None = None,
        organization: Any | None = None,
        request: Any | None = None,
    ) -> None:
        self.user = user
        self.organization = organization
        self.request = request

    # ------------------------------------------------------------------
    # Transactions
    # ------------------------------------------------------------------

    @staticmethod
    def atomic():
        """
        Database transaction decorator.
        """

        return transaction.atomic

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """
        Hook for subclasses.
        """

        return

    # ------------------------------------------------------------------
    # Permissions
    # ------------------------------------------------------------------

    def check_permissions(self) -> None:
        """
        Hook for subclasses.
        """

        return

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Execute the service.

        Subclasses must implement.
        """

        raise NotImplementedError(
            f"{self.__class__.__name__} must implement execute()."
        )

    # ------------------------------------------------------------------
    # Callable Interface
    # ------------------------------------------------------------------

    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Execute the service.
        """

        self.check_permissions()
        self.validate()

        return self.execute(
            *args,
            **kwargs,
        )

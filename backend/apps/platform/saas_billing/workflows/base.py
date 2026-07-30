"""
DatavionOS SaaS Billing workflow foundation.

Provides common workflow behavior:

- Transaction boundary
- Workflow execution lifecycle
- Logging
- Event publishing
- Error handling

Architecture:

API
 |
Workflow
 |
Service
 |
Model
 |
Domain Event
 |
Event Dispatcher
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from django.db import transaction

from apps.platform.saas_billing.events import (
    EventDispatcher,
)

logger = logging.getLogger(
    __name__,
)


class WorkflowError(
    Exception,
):
    """
    Base workflow exception.
    """


class BaseWorkflow(
    ABC,
):
    """
    Enterprise workflow base class.

    All SaaS billing workflows
    should inherit this class.
    """

    @transaction.atomic
    def execute(
        self,
        *args,
        **kwargs,
    ):
        """
        Execute workflow safely.

        Handles:

        - Database transaction
        - Logging
        - Exception wrapping
        """

        workflow_name = self.__class__.__name__

        try:
            logger.info(
                "Executing workflow: %s",
                workflow_name,
            )

            result = self.handle(
                *args,
                **kwargs,
            )

            logger.info(
                "Completed workflow: %s",
                workflow_name,
            )

            return result

        except Exception as exc:
            logger.exception(
                "Workflow failed: %s",
                workflow_name,
            )

            raise WorkflowError(
                str(exc),
            ) from exc

    @abstractmethod
    def handle(
        self,
        *args,
        **kwargs,
    ):
        """
        Workflow implementation.

        Must be implemented
        by child workflows.
        """

        raise NotImplementedError

    @staticmethod
    def publish_event(
        event,
    ) -> None:
        """
        Publish domain event.

        Example:

        SubscriptionCreated
        InvoicePaid
        PaymentSucceeded
        """

        EventDispatcher.dispatch(
            event,
        )


__all__ = [
    "BaseWorkflow",
    "WorkflowError",
]

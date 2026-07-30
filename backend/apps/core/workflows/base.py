"""
Base workflow.

Provides the reusable workflow orchestration foundation used
throughout the DatavionAI platform.
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import replace
from typing import Any, TypeVar

from django.db import transaction

from apps.core.events.base import DomainEvent
from apps.core.events.publisher import publisher
from apps.core.workflows.context import WorkflowContext
from apps.core.workflows.result import WorkflowResult

T = TypeVar("T")

logger = logging.getLogger(__name__)


class BaseWorkflow[T](
    ABC,
):
    """
    Base workflow.

    Every platform workflow should inherit from this class.

    Responsibilities:

    - Structured logging
    - Workflow timing
    - Event publishing
    - Post-commit scheduling
    - Background task dispatch
    - Standard execution lifecycle
    - Workflow payload handling
    """

    def __init__(
        self,
        *,
        logger_: logging.Logger | None = None,
        payload: Any | None = None,
    ) -> None:
        """
        Initialize workflow.

        Parameters
        ----------
        logger_
            Optional custom logger.

        payload
            Workflow input payload / request DTO.
        """

        self._logger = logger_ or logger
        self._payload = payload

    #
    # ------------------------------------------------------------------
    # Payload
    # ------------------------------------------------------------------
    #

    @property
    def payload(
        self,
    ) -> Any | None:
        """
        Return workflow payload.
        """

        return self._payload

    #
    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    #

    def log_started(
        self,
        *,
        context: WorkflowContext,
    ) -> None:
        """
        Log workflow start.
        """

        self._logger.info(
            "Workflow started.",
            extra=context.to_dict(),
        )

    def log_completed(
        self,
        *,
        context: WorkflowContext,
        duration_ms: int,
    ) -> None:
        """
        Log workflow completion.
        """

        payload = context.to_dict()

        payload["duration_ms"] = duration_ms

        self._logger.info(
            "Workflow completed.",
            extra=payload,
        )

    def log_failed(
        self,
        *,
        context: WorkflowContext,
        duration_ms: int,
        exception: Exception,
    ) -> None:
        """
        Log workflow failure.
        """

        payload = context.to_dict()

        payload["duration_ms"] = duration_ms

        self._logger.exception(
            "Workflow failed.",
            exc_info=exception,
            extra=payload,
        )

    #
    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    #

    def publish_event(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Publish a domain event immediately.
        """

        publisher.publish(event)

    def publish_after_commit(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Publish a domain event after transaction commit.
        """

        transaction.on_commit(
            lambda: publisher.publish(event),
        )

    #
    # ------------------------------------------------------------------
    # Background Tasks
    # ------------------------------------------------------------------
    #

    def dispatch_task(
        self,
        task: Callable[..., Any],
        /,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Execute a background task.

        Celery/Dramatiq/RQ integration can later replace direct
        invocation without changing workflow implementations.
        """

        try:
            task(
                *args,
                **kwargs,
            )

        except Exception:
            self._logger.exception(
                "Background task failed.",
            )

    def dispatch_after_commit(
        self,
        task: Callable[..., Any],
        /,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Dispatch a task after transaction commit.
        """

        transaction.on_commit(
            lambda: self.dispatch_task(
                task,
                *args,
                **kwargs,
            ),
        )

    #
    # ------------------------------------------------------------------
    # Timing
    # ------------------------------------------------------------------
    #

    @staticmethod
    def start_timer() -> float:
        """
        Start execution timer.
        """

        return time.perf_counter()

    @staticmethod
    def stop_timer(
        started_at: float,
    ) -> int:
        """
        Calculate workflow duration.
        """

        return int((time.perf_counter() - started_at) * 1000)

    #
    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------
    #

    def execute(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[T]:
        """
        Execute workflow lifecycle.

        Preserves workflow outcome.

        Important:
        WorkflowResult.fail() must remain failed.
        """

        started_at = self.start_timer()

        self.log_started(
            context=context,
        )

        try:
            result = self._run(
                context=context,
            )

            duration_ms = (
                result.duration_ms
                if result.duration_ms is not None
                else self.stop_timer(started_at)
            )

            self.log_completed(
                context=context,
                duration_ms=duration_ms,
            )

            #
            # Preserve original workflow state.
            #
            # Previous implementation converted:
            #
            # WorkflowResult.fail()
            #
            # into:
            #
            # WorkflowResult.ok()
            #
            # because it rebuilt every result as success.
            #
            # This breaks authorization failures.
            #
            if result.duration_ms is None:
                return replace(
                    result,
                    duration_ms=duration_ms,
                )

            return result

        except Exception as exc:
            duration_ms = self.stop_timer(
                started_at,
            )

            self.log_failed(
                context=context,
                duration_ms=duration_ms,
                exception=exc,
            )

            from apps.core.workflows.exceptions import (
                WorkflowExecutionError,
            )

            workflow_error = (
                exc
                if isinstance(
                    exc,
                    WorkflowExecutionError,
                )
                else WorkflowExecutionError(
                    str(exc),
                )
            )

            return WorkflowResult.fail(
                context=context,
                message=str(workflow_error),
                code=workflow_error.code,
                error=workflow_error,
                duration_ms=duration_ms,
            )

    #
    # ------------------------------------------------------------------
    # Abstract API
    # ------------------------------------------------------------------
    #

    @abstractmethod
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[T]:
        """
        Execute workflow implementation.

        Business rules belong in services.

        Authorization belongs in policies.

        Persistence belongs in services/repositories.
        """

        raise NotImplementedError


__all__: tuple[str, ...] = ("BaseWorkflow",)

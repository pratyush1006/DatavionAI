"""Workflow orchestration for Revenue Cycle cross-module integration."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from .policies import CrossModuleIntegrationPolicy
from .services import CrossModuleIntegrationService


class CrossModuleIntegrationWorkflow:
    """Orchestrate authorized integration operations."""

    @staticmethod
    def ingest(
        *,
        user: Any,
        organization: Any,
        event_type: str,
        source: str,
        event_name: str,
        aggregate_id: UUID,
        idempotency_key: str,
        payload: dict[str, Any],
    ) -> Any:
        """Authorize and ingest an integration record."""

        if not CrossModuleIntegrationPolicy.can_process(
            user=user,
            organization=organization,
        ):
            raise PermissionError(
                "Revenue Cycle integration processing permission is required."
            )

        return CrossModuleIntegrationService.ingest(
            organization=organization,
            event_type=event_type,
            source=source,
            event_name=event_name,
            aggregate_id=aggregate_id,
            idempotency_key=idempotency_key,
            payload=payload,
            actor=user,
        )

    @staticmethod
    def process(
        *,
        user: Any,
        organization: Any,
        record_id: UUID,
    ) -> Any:
        """Authorize and process an integration record."""

        if not CrossModuleIntegrationPolicy.can_process(
            user=user,
            organization=organization,
        ):
            raise PermissionError(
                "Revenue Cycle integration processing permission is required."
            )

        return CrossModuleIntegrationService.process(
            organization=organization,
            record_id=record_id,
            actor=user,
        )


__all__ = ("CrossModuleIntegrationWorkflow",)

"""Transactional services for Revenue Cycle cross-module integration."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from django.db import IntegrityError, transaction
from django.utils import timezone

from .constants import IntegrationRecordStatus
from .events import publish_integration_event
from .models import RevenueCycleIntegrationRecord


class CrossModuleIntegrationService:
    """Persist and process organization-scoped integration messages."""

    @staticmethod
    @transaction.atomic
    def ingest(
        *,
        organization: Any,
        event_type: str,
        source: str,
        event_name: str,
        aggregate_id: UUID,
        idempotency_key: str,
        payload: dict[str, Any],
        actor: Any = None,
    ) -> RevenueCycleIntegrationRecord:
        """Create one integration record, returning an existing idempotent record."""

        if not idempotency_key:
            raise ValueError("idempotency_key is required.")
        if not event_name:
            raise ValueError("event_name is required.")
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object.")

        existing = RevenueCycleIntegrationRecord.objects.filter(
            organization=organization,
            idempotency_key=idempotency_key,
        ).first()
        if existing:
            return existing

        try:
            record = RevenueCycleIntegrationRecord.objects.create(
                organization=organization,
                event_type=event_type,
                source=source,
                event_name=event_name,
                aggregate_id=aggregate_id,
                idempotency_key=idempotency_key,
                payload=payload,
                created_by=actor,
            )
        except IntegrityError:
            record = RevenueCycleIntegrationRecord.objects.get(
                organization=organization,
                idempotency_key=idempotency_key,
            )

        publish_integration_event(
            event_type="revenue_cycle.integration.record_ingested",
            aggregate_id=record.id,
            payload={
                "organization_id": str(organization.id),
                "event_name": record.event_name,
                "source": record.source,
                "status": record.status,
            },
        )
        return record

    @staticmethod
    @transaction.atomic
    def process(
        *,
        organization: Any,
        record_id: UUID,
        actor: Any,
    ) -> RevenueCycleIntegrationRecord:
        """Process a pending integration record with row-level locking."""

        record = RevenueCycleIntegrationRecord.objects.select_for_update().get(
            organization_id=organization.id,
            id=record_id,
        )

        if record.status == IntegrationRecordStatus.PROCESSED:
            return record
        if record.status == IntegrationRecordStatus.IGNORED:
            raise ValueError("Ignored integration records cannot be processed.")

        record.attempts += 1

        try:
            CrossModuleIntegrationService._validate_payload(record)
        except ValueError as exc:
            record.status = IntegrationRecordStatus.FAILED
            record.last_error = str(exc)
            record.save(
                update_fields=[
                    "status",
                    "last_error",
                    "attempts",
                    "updated_at",
                ]
            )
            raise

        record.status = IntegrationRecordStatus.PROCESSED
        record.last_error = ""
        record.processed_at = timezone.now()
        record.save(
            update_fields=[
                "status",
                "last_error",
                "processed_at",
                "attempts",
                "updated_at",
            ]
        )

        publish_integration_event(
            event_type="revenue_cycle.integration.record_processed",
            aggregate_id=record.id,
            payload={
                "organization_id": str(organization.id),
                "processed_by": str(actor.id),
                "event_name": record.event_name,
                "attempts": record.attempts,
            },
        )
        return record

    @staticmethod
    def _validate_payload(
        record: RevenueCycleIntegrationRecord,
    ) -> None:
        """Validate the minimum envelope required for processing."""

        required = {
            "event_name": record.event_name,
            "event_type": record.event_type,
            "source": record.source,
        }
        if any(not value for value in required.values()):
            raise ValueError("Integration event envelope is incomplete.")


__all__ = ("CrossModuleIntegrationService",)

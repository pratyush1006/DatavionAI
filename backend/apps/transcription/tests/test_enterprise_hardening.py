from __future__ import annotations

from django.apps import apps
from django.test import TestCase

from apps.transcription.models import (
    TranscriptionIdempotencyKey,
    TranscriptionOutboxEvent,
)
from apps.transcription.services.idempotency import get_or_create
from apps.transcription.services.outbox import enqueue_event


class TranscriptionEnterpriseHardeningTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tenant = apps.get_model("tenancy", "Tenant")
        Organization = apps.get_model("organizations", "Organization")
        cls.tenant = Tenant.objects.create(
            name="Transcription Enterprise Tenant",
            slug="transcription-enterprise-tenant",
        )
        cls.organization = Organization.objects.create(
            tenant=cls.tenant,
            name="Transcription Enterprise Org",
            code="TRANS-ENT",
            slug="transcription-enterprise-org",
        )

    def test_idempotency_rejects_payload_reuse(self):
        get_or_create(
            organization=self.organization,
            scope="job.create",
            key="abc",
            payload={"x": 1},
        )
        with self.assertRaises(ValueError):
            get_or_create(
                organization=self.organization,
                scope="job.create",
                key="abc",
                payload={"x": 2},
            )
        self.assertEqual(TranscriptionIdempotencyKey.objects.count(), 1)

    def test_outbox_is_tenant_scoped(self):
        event = enqueue_event(
            organization=self.organization,
            event_type="transcription.test",
            aggregate_type="test",
            aggregate_id="1",
            payload={"ok": True},
        )
        self.assertEqual(event.organization_id, self.organization.pk)
        self.assertEqual(
            TranscriptionOutboxEvent.objects.filter(
                organization=self.organization
            ).count(),
            1,
        )

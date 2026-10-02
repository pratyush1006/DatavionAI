from django.apps import apps
from django.test import TestCase

from apps.notes.models import NoteIdempotencyKey, NoteOutboxEvent
from apps.notes.services.idempotency import get_or_create
from apps.notes.services.outbox import enqueue_event


class NotesEnterpriseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tenant = apps.get_model("tenancy", "Tenant")
        Organization = apps.get_model("organizations", "Organization")
        cls.tenant = Tenant.objects.create(
            name="Notes Enterprise Tenant", slug="notes-enterprise-tenant"
        )
        cls.organization = Organization.objects.create(
            tenant=cls.tenant,
            name="Notes Enterprise Org",
            code="NOTES-ENT",
            slug="notes-enterprise-org",
        )

    def test_idempotency_payload_mismatch_rejected(self):
        get_or_create(
            organization=self.organization,
            scope="note.create",
            key="abc",
            payload={"x": 1},
        )
        with self.assertRaises(ValueError):
            get_or_create(
                organization=self.organization,
                scope="note.create",
                key="abc",
                payload={"x": 2},
            )
        self.assertEqual(NoteIdempotencyKey.objects.count(), 1)

    def test_outbox_tenant_scoped(self):
        event = enqueue_event(
            organization=self.organization,
            event_type="notes.test",
            aggregate_type="ClinicalNote",
            aggregate_id="1",
            payload={"ok": True},
        )
        self.assertEqual(event.organization_id, self.organization.id)
        self.assertEqual(
            NoteOutboxEvent.objects.filter(organization=self.organization).count(), 1
        )

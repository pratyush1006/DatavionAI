from django.test import SimpleTestCase

from apps.notes.events.note_events import (
    ClinicalNoteAmendedEvent,
    ClinicalNoteCancelledEvent,
    ClinicalNoteCreatedEvent,
    ClinicalNoteReviewedEvent,
    ClinicalNoteSignedEvent,
)


class ClinicalNoteDomainEventTests(SimpleTestCase):
    def test_lifecycle_events_are_first_class_contracts(self):
        for event_cls in (
            ClinicalNoteCreatedEvent,
            ClinicalNoteReviewedEvent,
            ClinicalNoteSignedEvent,
            ClinicalNoteAmendedEvent,
            ClinicalNoteCancelledEvent,
        ):
            self.assertTrue(event_cls.__name__.endswith("Event"))

    def test_event_payload_contracts_are_tenant_organization_patient_scoped(self):
        required = {"note_id", "organization_id", "patient_id"}
        for event_cls in (
            ClinicalNoteCreatedEvent,
            ClinicalNoteReviewedEvent,
            ClinicalNoteSignedEvent,
            ClinicalNoteAmendedEvent,
            ClinicalNoteCancelledEvent,
        ):
            self.assertTrue(
                required.issubset(event_cls.__dataclass_fields__), event_cls.__name__
            )

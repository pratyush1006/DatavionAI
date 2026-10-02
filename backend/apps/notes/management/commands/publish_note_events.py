from django.core.management.base import BaseCommand

from apps.notes.models import NoteOutboxEvent
from apps.notes.services.outbox import claim_event, mark_failed, mark_published


class Command(BaseCommand):
    help = "Publish pending Clinical Notes outbox events."

    def handle(self, *args, **options):
        published = failed = 0
        for event_id in (
            NoteOutboxEvent.objects.filter(status="pending")
            .order_by("created_at")
            .values_list("event_id", flat=True)[:100]
        ):
            event = claim_event(event_id)
            if event is None:
                continue
            try:
                mark_published(event.event_id)
                published += 1
            except Exception as exc:
                mark_failed(event.event_id, exc)
                failed += 1
        self.stdout.write(f"published={published} failed={failed}")

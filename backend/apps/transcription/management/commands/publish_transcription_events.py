from __future__ import annotations

from apps.transcription.models import TranscriptionOutboxEvent
from apps.transcription.services.outbox import claim_event, mark_failed, mark_published
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Publish pending Transcription outbox events."

    def handle(self, *args, **options):
        published = failed = 0
        for event_id in (
            TranscriptionOutboxEvent.objects.filter(status="pending")
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
                mark_failed(event.event_id, str(exc))
                failed += 1
        self.stdout.write(f"published={published} failed={failed}")

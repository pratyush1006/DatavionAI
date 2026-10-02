from django.conf import settings
from django.core.management.base import BaseCommand

from apps.clinical.medications.services.events import publish_pending_events


def configured_publisher(envelope):
    # Integration point. Production deployments should replace this with the
    # configured event transport adapter.
    return envelope


class Command(BaseCommand):
    help = "Publish pending Medication outbox events."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        if not getattr(settings, "MEDICATION_EVENT_PUBLISHER", ""):
            self.stderr.write("MEDICATION_EVENT_PUBLISHER is not configured.")
            raise SystemExit(1)
        count = publish_pending_events(
            limit=options["limit"],
            publisher=configured_publisher,
        )
        self.stdout.write(f"PUBLISHED: {count}")

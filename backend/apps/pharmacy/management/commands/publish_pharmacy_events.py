from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string

from apps.pharmacy.services.events import publish_pending_events


class Command(BaseCommand):
    help = "Publish committed Pharmacy outbox events through the configured broker adapter."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        publisher_path = getattr(settings, "PHARMACY_EVENT_PUBLISHER", "")
        if not publisher_path:
            raise CommandError(
                "PHARMACY_EVENT_PUBLISHER is not configured. Configure a dotted-path callable that accepts an event envelope."
            )
        try:
            publisher = import_string(publisher_path)
        except (ImportError, AttributeError) as exc:
            raise CommandError(f"Invalid PHARMACY_EVENT_PUBLISHER: {exc}") from exc
        count = publish_pending_events(limit=options["limit"], publisher=publisher)
        self.stdout.write(
            self.style.SUCCESS(f"Published {count} pharmacy outbox event(s).")
        )

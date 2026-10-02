from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string

from apps.imaging.services.events import publish_pending_events


class Command(BaseCommand):
    help = "Publish committed Imaging outbox events."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        path = getattr(settings, "IMAGING_EVENT_PUBLISHER", "")
        if not path:
            raise CommandError("IMAGING_EVENT_PUBLISHER is not configured.")
        try:
            publisher = import_string(path)
        except (ImportError, AttributeError) as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(
            self.style.SUCCESS(
                f"Published {publish_pending_events(limit=options['limit'], publisher=publisher)} Imaging outbox event(s)."
            )
        )

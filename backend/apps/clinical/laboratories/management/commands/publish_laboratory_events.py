from django.core.management.base import BaseCommand, CommandError

from apps.clinical.laboratories.services.events import publish_pending_events


class Command(BaseCommand):
    help = "Publish pending Laboratory outbox events."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        limit = options["limit"]
        if limit <= 0:
            raise CommandError("--limit must be greater than zero.")
        count = publish_pending_events(limit=limit)
        self.stdout.write(
            self.style.SUCCESS(f"Published {count} laboratory outbox event(s).")
        )

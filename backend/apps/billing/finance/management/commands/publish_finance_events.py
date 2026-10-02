from django.core.management.base import BaseCommand

from apps.billing.finance.services.events import publish_pending_events


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        count = publish_pending_events(limit=max(1, options["limit"]))
        self.stdout.write(self.style.SUCCESS(f"Published {count} Finance events."))

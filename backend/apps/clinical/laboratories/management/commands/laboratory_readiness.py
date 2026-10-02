from django.core.management.base import BaseCommand

from apps.clinical.laboratories.services.events import laboratory_readiness


class Command(BaseCommand):
    help = "Check Laboratory production readiness."

    def handle(self, *args, **options):
        self.stdout.write(str(laboratory_readiness()))

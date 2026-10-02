from django.core.management.base import BaseCommand

from apps.clinical.medications.services.production_readiness import (
    medication_production_readiness,
)


class Command(BaseCommand):
    help = "Run the Medication production-readiness audit."

    def handle(self, *args, **options):
        result = medication_production_readiness()
        for name, passed in result["checks"].items():
            self.stdout.write(f"{name}: {'PASS' if passed else 'FAIL'}")
        if not result["ready"]:
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS("MEDICATION_PRODUCTION_READINESS: PASS"))

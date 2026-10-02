import json

from django.core.management.base import BaseCommand, CommandError

from apps.pharmacy.services.production_readiness import production_readiness_report


class Command(BaseCommand):
    help = "Validate DatavionOS production configuration required by Pharmacy."

    def add_arguments(self, parser):
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Exit non-zero when any production gate fails.",
        )

    def handle(self, *args, **options):
        try:
            report = production_readiness_report(strict=False)
        except Exception as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(json.dumps(report, indent=2, sort_keys=True))
        if options["strict"] and report["status"] != "ready":
            raise CommandError(
                "Production readiness gates failed. Configure the reported settings and rerun with --strict."
            )
        if report["status"] == "ready":
            self.stdout.write(
                self.style.SUCCESS("PHARMACY_PRODUCTION_READINESS: READY")
            )
        else:
            self.stdout.write(
                self.style.WARNING("PHARMACY_PRODUCTION_READINESS: NOT_READY")
            )

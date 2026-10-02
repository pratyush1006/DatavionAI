from django.core.management.base import BaseCommand, CommandError

from apps.common.storage.production import storage_readiness


class Command(BaseCommand):
    help = "Evaluate DatavionOS storage production readiness."

    def add_arguments(self, parser):
        parser.add_argument("--probe", action="store_true")
        parser.add_argument("--strict", action="store_true")

    def handle(self, *args, **options):
        result = storage_readiness(perform_probe=options["probe"])
        self.stdout.write(f"environment: {result.environment}")
        self.stdout.write(f"backend: {result.backend or '<unconfigured>'}")
        self.stdout.write(f"configured: {result.configured}")
        self.stdout.write(f"production_safe: {result.production_safe}")
        self.stdout.write(f"path_safe: {result.path_safe}")
        self.stdout.write(f"upload_policy_ready: {result.upload_policy_ready}")
        for warning in result.warnings:
            self.stdout.write(self.style.WARNING(f"WARNING: {warning}"))
        for error in result.errors:
            self.stdout.write(self.style.ERROR(f"ERROR: {error}"))
        if result.errors or (options["strict"] and result.warnings):
            raise CommandError("Storage readiness check failed.")
        self.stdout.write(self.style.SUCCESS("STORAGE_READINESS: PASS"))

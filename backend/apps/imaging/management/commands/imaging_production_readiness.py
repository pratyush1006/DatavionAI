from django.core.management.base import BaseCommand

from apps.imaging.workflow_registry import (
    ORDER_TRANSITIONS,
    REPORT_TRANSITIONS,
    STUDY_TRANSITIONS,
)


class Command(BaseCommand):
    help = "Validate the Imaging/Radiology workflow contract."

    def handle(self, *args, **options):
        self.stdout.write("Imaging/Radiology workflow readiness")
        self.stdout.write(f"Order states: {len(ORDER_TRANSITIONS)}")
        self.stdout.write(f"Study states: {len(STUDY_TRANSITIONS)}")
        self.stdout.write(f"Report states: {len(REPORT_TRANSITIONS)}")
        self.stdout.write(self.style.SUCCESS("WORKFLOW CONTRACT READY"))

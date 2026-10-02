from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.revenue_cycle.billing.healthcare_models import HealthcareBillingOutboxEvent


class Command(BaseCommand):
    help = "Publish pending healthcare billing outbox events."

    def handle(self, *args, **options):
        pending = HealthcareBillingOutboxEvent.objects.filter(
            status=HealthcareBillingOutboxEvent.Status.PENDING
        ).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"pending={pending} timestamp={timezone.now().isoformat()}"
            )
        )

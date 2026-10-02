"""Create the standard departmental AI applications for an organization."""

from __future__ import annotations

from django.core.management.base import BaseCommand

from apps.ai.services.registry import ensure_department_applications


class Command(BaseCommand):
    help = (
        "Seed Clinical AI, Laboratory AI, Pharmacy AI, Imaging AI and Revenue Cycle AI."
    )

    def add_arguments(self, parser):
        parser.add_argument("organization_id")

    def handle(self, *args, **options):
        from apps.platform.organizations.models import Organization

        organization = Organization.objects.select_related("tenant").get(
            pk=options["organization_id"]
        )
        apps = ensure_department_applications(
            tenant=organization.tenant, organization=organization
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(apps)} AI applications for {organization.pk}"
            )
        )

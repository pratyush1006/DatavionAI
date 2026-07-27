"""
Seed default DatavionOS subscription plans.

Creates:

Clinic Starter
Clinic Professional
Clinic Enterprise
Hospital Enterprise

with module and feature entitlements.
"""

from __future__ import annotations

from decimal import Decimal

from django.core.management.base import (
    BaseCommand,
)

from apps.platform.subscriptions.models import (
    FeatureEntitlement,
    ModuleEntitlement,
    SubscriptionPlan,
)

PLANS = (
    {
        "name": "Clinic Starter",
        "code": "clinic_starter",
        "description": ("Starter plan for small clinics."),
        "price": Decimal("999"),
        "billing_cycle": "monthly",
        "modules": [
            "appointment-management",
        ],
        "features": [
            "dashboard",
            "notifications",
            "search",
        ],
    },
    {
        "name": "Clinic Professional",
        "code": "clinic_professional",
        "description": ("Professional plan for growing clinics."),
        "price": Decimal("2999"),
        "billing_cycle": "monthly",
        "modules": [
            "appointment-management",
            "ai-assistant",
        ],
        "features": [
            "dashboard",
            "notifications",
            "search",
            "ai_assistant",
        ],
    },
    {
        "name": "Clinic Enterprise",
        "code": "clinic_enterprise",
        "description": ("Enterprise AI powered clinic platform."),
        "price": Decimal("9999"),
        "billing_cycle": "monthly",
        "modules": [
            "appointment-management",
            "ai-assistant",
            "ai-workflow",
        ],
        "features": [
            "dashboard",
            "notifications",
            "search",
            "ai_assistant",
            "ai_workflows",
        ],
    },
    {
        "name": "Hospital Enterprise",
        "code": "hospital_enterprise",
        "description": ("Complete hospital operating system."),
        "price": Decimal("24999"),
        "billing_cycle": "monthly",
        "modules": [
            "appointment-management",
            "ai-assistant",
            "ai-workflow",
        ],
        "features": [
            "dashboard",
            "notifications",
            "search",
            "ai_assistant",
            "ai_workflows",
            "analytics",
        ],
    },
)


class Command(BaseCommand):
    """
    Seed subscription catalog.
    """

    help = "Create default DatavionOS subscription plans."

    def handle(
        self,
        *args,
        **options,
    ):

        for data in PLANS:
            plan, created = SubscriptionPlan.objects.update_or_create(
                code=data["code"],
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "price": data["price"],
                    "billing_cycle": data["billing_cycle"],
                    "is_active": True,
                },
            )

            ModuleEntitlement.objects.filter(
                plan=plan,
            ).delete()

            FeatureEntitlement.objects.filter(
                plan=plan,
            ).delete()

            ModuleEntitlement.objects.bulk_create(
                [
                    ModuleEntitlement(
                        plan=plan,
                        module_identifier=module,
                        enabled=True,
                    )
                    for module in data["modules"]
                ]
            )

            FeatureEntitlement.objects.bulk_create(
                [
                    FeatureEntitlement(
                        plan=plan,
                        feature_key=feature,
                        enabled=True,
                    )
                    for feature in data["features"]
                ]
            )

            status = "created" if created else "updated"

            self.stdout.write(self.style.SUCCESS(f"{plan.name} {status}"))

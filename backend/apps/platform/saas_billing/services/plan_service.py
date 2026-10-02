"""
SaaS Billing Plan services.

Business logic layer for DatavionOS SaaS plans.

Responsibilities:

- Create plans
- Update plans
- Activate plans
- Deactivate plans
- Archive plans

Architecture:

Workflow
      |
PlanService
      |
Plan Manager
      |
Plan Model
      |
Domain Event
"""

from __future__ import annotations

from django.db import transaction

from apps.platform.saas_billing.models import (
    Plan,
)


class PlanService:
    """
    Enterprise SaaS plan service.
    """

    @staticmethod
    @transaction.atomic
    def create_plan(
        *,
        data: dict,
    ) -> Plan:
        """
        Create SaaS plan.
        """

        existing = Plan.objects.filter(
            code=data.get(
                "code",
            ),
        ).first()

        if existing:
            return existing

        return Plan.objects.create(
            **data,
        )

    @staticmethod
    @transaction.atomic
    def update_plan(
        *,
        plan: Plan,
        data: dict,
    ) -> Plan:
        """
        Update SaaS plan.
        """

        allowed_fields = {
            "name",
            "description",
            "price",
            "currency",
            "billing_cycle",
            "features",
            "modules",
            "limits",
            "metadata",
            "is_public",
            "is_featured",
            "display_order",
        }

        updated_fields = []

        for field, value in data.items():
            if field in allowed_fields:
                setattr(
                    plan,
                    field,
                    value,
                )

                updated_fields.append(
                    field,
                )

        if updated_fields:
            updated_fields.append(
                "updated_at",
            )

            plan.save(
                update_fields=updated_fields,
            )

        return plan

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        plan: Plan,
    ) -> Plan:
        """
        Activate plan.
        """

        plan.is_active = True

        plan.save(
            update_fields=[
                "is_active",
                "updated_at",
            ],
        )

        return plan

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        plan: Plan,
    ) -> Plan:
        """
        Deactivate plan.
        """

        plan.is_active = False

        plan.save(
            update_fields=[
                "is_active",
                "updated_at",
            ],
        )

        return plan

    @staticmethod
    @transaction.atomic
    def archive(
        *,
        plan: Plan,
    ) -> Plan:
        """
        Archive plan.
        """

        plan.is_active = False

        plan.save(
            update_fields=[
                "is_active",
                "updated_at",
            ],
        )

        return plan


__all__ = [
    "PlanService",
]

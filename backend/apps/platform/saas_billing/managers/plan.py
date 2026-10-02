"""
SaaS Plan managers.

Provides reusable queryset operations
for DatavionOS subscription plans.

Responsibilities:

- Active plan discovery
- Public subscription plans
- Healthcare segment filtering
- Pricing queries
- Feature/module entitlement lookup
- Subscription eligibility
- Enterprise plan discovery
"""

from __future__ import annotations

from decimal import Decimal

from django.db import models


class PlanQuerySet(
    models.QuerySet,
):
    """
    QuerySet helpers for SaaS plans.
    """

    # --------------------------------------------------------------
    # Lifecycle
    # --------------------------------------------------------------

    def active(
        self,
    ):
        """
        Return active plans.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ):
        """
        Return inactive plans.
        """

        return self.filter(
            is_active=False,
        )

    def public(
        self,
    ):
        """
        Return customer selectable plans.
        """

        return self.filter(
            is_active=True,
            is_public=True,
        )

    def custom(
        self,
    ):
        """
        Return custom enterprise plans.
        """

        return self.filter(
            is_custom=True,
        )

    # --------------------------------------------------------------
    # Billing Cycle
    # --------------------------------------------------------------

    def monthly(
        self,
    ):
        """
        Return monthly billing plans.
        """

        return self.filter(
            billing_cycle="monthly",
        )

    def yearly(
        self,
    ):
        """
        Return yearly billing plans.
        """

        return self.filter(
            billing_cycle="yearly",
        )

    # --------------------------------------------------------------
    # Pricing
    # --------------------------------------------------------------

    def currency(
        self,
        currency: str,
    ):
        """
        Filter plans by currency.
        """

        return self.filter(
            currency=currency,
        )

    def free(
        self,
    ):
        """
        Return free plans.
        """

        return self.filter(
            price=0,
        )

    def paid(
        self,
    ):
        """
        Return paid plans.
        """

        return self.filter(
            price__gt=0,
        )

    def price_range(
        self,
        minimum: Decimal | int = 0,
        maximum: Decimal | int | None = None,
    ):
        """
        Filter plans by price range.
        """

        queryset = self.filter(
            price__gte=minimum,
        )

        if maximum is not None:
            queryset = queryset.filter(
                price__lte=maximum,
            )

        return queryset

    # --------------------------------------------------------------
    # Plan Type
    # --------------------------------------------------------------

    def starter(
        self,
    ):
        """
        Return starter plans.
        """

        return self.filter(
            plan_type="STARTER",
        )

    def professional(
        self,
    ):
        """
        Return professional plans.
        """

        return self.filter(
            plan_type="PROFESSIONAL",
        )

    def business(
        self,
    ):
        """
        Return business plans.
        """

        return self.filter(
            plan_type="BUSINESS",
        )

    def enterprise(
        self,
    ):
        """
        Return enterprise plans.
        """

        return self.filter(
            plan_type="ENTERPRISE",
        )

    # --------------------------------------------------------------
    # Healthcare Segments
    # --------------------------------------------------------------

    def healthcare_segment(
        self,
        segment: str,
    ):
        """
        Filter healthcare vertical plans.
        """

        return self.filter(
            healthcare_segment=segment,
        )

    def hospitals(
        self,
    ):
        return self.healthcare_segment(
            "HOSPITAL",
        )

    def clinics(
        self,
    ):
        return self.healthcare_segment(
            "CLINIC",
        )

    def pharmacies(
        self,
    ):
        return self.healthcare_segment(
            "PHARMACY",
        )

    def laboratories(
        self,
    ):
        return self.healthcare_segment(
            "LABORATORY",
        )

    # --------------------------------------------------------------
    # Entitlements
    # --------------------------------------------------------------

    def with_module(
        self,
        module: str,
    ):
        """
        Return plans enabling module.
        """

        return self.filter(
            modules__has_key=module,
        )

    def with_feature(
        self,
        feature: str,
    ):
        """
        Return plans enabling feature.
        """

        return self.filter(
            features__has_key=feature,
        )

    def supports_ai(
        self,
    ):
        """
        Return AI enabled plans.
        """

        return self.filter(
            modules__has_key="ai",
        )

    def supports_telemedicine(
        self,
    ):
        """
        Return telemedicine enabled plans.
        """

        return self.filter(
            modules__has_key="telemedicine",
        )

    def supports_pharmacy(
        self,
    ):
        """
        Return pharmacy enabled plans.
        """

        return self.filter(
            modules__has_key="pharmacy",
        )

    # --------------------------------------------------------------
    # Capacity
    # --------------------------------------------------------------

    def supports_users(
        self,
        count: int,
    ):
        """
        Return plans supporting users.
        """

        return self.filter(
            max_users__gte=count,
        )

    def supports_patients(
        self,
        count: int,
    ):
        """
        Return plans supporting patients.
        """

        return self.filter(
            max_patients__gte=count,
        )

    def supports_storage(
        self,
        storage_gb: int,
    ):
        """
        Return plans supporting storage.
        """

        return self.filter(
            max_storage_gb__gte=storage_gb,
        )

    # --------------------------------------------------------------
    # Signup / Default Selection
    # --------------------------------------------------------------

    def default(
        self,
    ):
        """
        Return default onboarding plan.

        Used during organization signup.
        """

        return (
            self.active()
            .public()
            .order_by(
                "price",
                "created_at",
            )
            .first()
        )

    def cheapest(
        self,
    ):
        """
        Return lowest priced plan.
        """

        return (
            self.active()
            .order_by(
                "price",
            )
            .first()
        )

    def premium(
        self,
    ):
        """
        Return highest tier plans.
        """

        return self.active().order_by(
            "-price",
        )


class PlanManager(
    models.Manager,
):
    """
    Manager for SaaS Plan model.
    """

    def get_queryset(
        self,
    ):
        return PlanQuerySet(
            self.model,
            using=self._db,
        )

    def default_plan(
        self,
    ):
        """
        Return default signup plan.
        """

        return self.get_queryset().default()


__all__ = [
    "PlanManager",
    "PlanQuerySet",
]

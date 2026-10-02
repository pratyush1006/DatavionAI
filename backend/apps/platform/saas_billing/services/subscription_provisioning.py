"""
DatavionOS subscription provisioning service.

This service resolves an existing SaaS Plan from the canonical
organization pricing catalog and creates the organization's
Subscription.

The service never creates pricing plans.

Pricing authority:

    Category
        +
    Organization Type
        +
    Organization Size
        +
    Commercial Tier
        |
        v
    Existing Plan
        |
        v
    Subscription
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.platform.saas_billing.models.plan import Plan
from apps.platform.saas_billing.models.subscription import Subscription


class SubscriptionProvisioningError(Exception):
    """Base provisioning exception."""


class PlanResolutionError(SubscriptionProvisioningError):
    """Raised when the requested pricing combination cannot be resolved."""


class SubscriptionAlreadyExistsError(SubscriptionProvisioningError):
    """Raised when an organization already owns a subscription."""


class SubscriptionProvisioningService:
    """
    Canonical DatavionOS subscription provisioning service.

    The service consumes the already-created pricing catalog.

    No plan is created here.
    """

    @staticmethod
    def _normalize(value: Any) -> str:
        if value is None:
            return ""

        value = str(value).strip().lower()

        value = re.sub(r"[_\-/]+", " ", value)
        value = re.sub(r"\s+", " ", value)

        return value.strip()

    @classmethod
    def _flatten_metadata(
        cls,
        value: Any,
        output: list[str],
    ) -> None:
        """
        Recursively collect normalized metadata values.

        This makes provisioning resilient to small catalog metadata
        representation differences.
        """

        if isinstance(value, dict):
            for key, item in value.items():
                output.append(cls._normalize(key))

                if isinstance(item, (dict, list, tuple)):
                    cls._flatten_metadata(item, output)
                else:
                    output.append(cls._normalize(item))

            return

        if isinstance(value, (list, tuple)):
            for item in value:
                cls._flatten_metadata(item, output)

            return

        output.append(cls._normalize(value))

    @classmethod
    def _plan_matches(
        cls,
        plan: Plan,
        *,
        category: str,
        organization_type: str,
        size: str,
        tier: str,
    ) -> bool:
        """
        Determine whether a catalog plan represents the requested
        organization/category/size/tier combination.

        The canonical installer stores catalog information in plan
        metadata. The resolver also supports common aliases so the
        provisioning service remains compatible with the existing
        catalog.
        """

        required = {
            cls._normalize(category),
            cls._normalize(organization_type),
            cls._normalize(size),
            cls._normalize(tier),
        }

        if not all(required):
            return False

        metadata = getattr(plan, "metadata", {}) or {}

        if not isinstance(metadata, dict):
            metadata = {}

        normalized_values: list[str] = []

        cls._flatten_metadata(
            metadata,
            normalized_values,
        )

        direct_values = [
            getattr(plan, "code", ""),
            getattr(plan, "name", ""),
            getattr(plan, "healthcare_segment", ""),
            getattr(plan, "plan_type", ""),
        ]

        normalized_values.extend(
            cls._normalize(value) for value in direct_values if value
        )

        value_set = set(normalized_values)

        # Exact metadata/value matching.
        if required.issubset(value_set):
            return True

        # Some catalog values can contain a compound string.
        compound_text = " ".join(normalized_values)

        return all(token in compound_text for token in required)

    @classmethod
    def resolve_plan(
        cls,
        *,
        category: str,
        organization_type: str,
        size: str,
        tier: str,
    ) -> Plan:
        """
        Resolve one existing plan from the canonical pricing catalog.
        """

        category = cls._normalize(category)
        organization_type = cls._normalize(organization_type)
        size = cls._normalize(size)
        tier = cls._normalize(tier)

        if not all(
            (
                category,
                organization_type,
                size,
                tier,
            )
        ):
            raise PlanResolutionError(
                "Category, organization_type, size and tier are all required."
            )

        candidates = list(
            Plan.objects.filter(
                is_active=True,
                is_public=True,
            ).order_by(
                "display_order",
                "created_at",
            )
        )

        matches = [
            plan
            for plan in candidates
            if cls._plan_matches(
                plan,
                category=category,
                organization_type=organization_type,
                size=size,
                tier=tier,
            )
        ]

        if not matches:
            raise PlanResolutionError(
                "No active public pricing plan was found for "
                f"category={category!r}, "
                f"organization_type={organization_type!r}, "
                f"size={size!r}, "
                f"tier={tier!r}."
            )

        if len(matches) > 1:
            # Prefer an exact custom/catalog metadata match before
            # failing because of ambiguity.
            exact = []

            for plan in matches:
                metadata = getattr(plan, "metadata", {}) or {}

                if not isinstance(metadata, dict):
                    continue

                normalized_metadata = {
                    cls._normalize(key): cls._normalize(value)
                    for key, value in metadata.items()
                    if not isinstance(value, (dict, list))
                }

                if (
                    normalized_metadata.get("category") == category
                    and normalized_metadata.get("organization_type")
                    == organization_type
                    and normalized_metadata.get("size") == size
                    and normalized_metadata.get("tier") == tier
                ):
                    exact.append(plan)

            if len(exact) == 1:
                return exact[0]

            raise PlanResolutionError(
                "Multiple pricing plans matched the requested "
                "organization context. The catalog must contain "
                "one unambiguous plan."
            )

        return matches[0]

    @staticmethod
    def _plan_snapshot(plan: Plan) -> dict[str, Any]:
        """
        Freeze commercial configuration at subscription creation.
        """

        return {
            "id": str(plan.id),
            "name": plan.name,
            "code": plan.code,
            "description": plan.description,
            "plan_type": plan.plan_type,
            "healthcare_segment": plan.healthcare_segment,
            "price": str(plan.price),
            "setup_fee": str(plan.setup_fee),
            "currency": plan.currency,
            "billing_cycle": plan.billing_cycle,
            "trial_days": plan.trial_days,
            "annual_discount_percentage": (plan.annual_discount_percentage),
            "max_users": plan.max_users,
            "max_branches": plan.max_branches,
            "max_doctors": plan.max_doctors,
            "max_patients": plan.max_patients,
            "max_lab_orders": plan.max_lab_orders,
            "max_imaging_orders": plan.max_imaging_orders,
            "max_pharmacy_products": plan.max_pharmacy_products,
            "max_inventory_transactions": (plan.max_inventory_transactions),
            "max_storage_gb": plan.max_storage_gb,
            "max_api_requests": plan.max_api_requests,
            "max_ai_requests": plan.max_ai_requests,
            "max_ai_tokens": plan.max_ai_tokens,
            "features": plan.features or {},
            "modules": plan.modules or {},
            "limits": plan.limits or {},
            "metadata": plan.metadata or {},
            "is_custom": plan.is_custom,
        }

    @staticmethod
    def _feature_snapshot(plan: Plan) -> dict[str, Any]:
        return {
            "features": plan.features or {},
            "modules": plan.modules or {},
            "limits": plan.limits or {},
        }

    @staticmethod
    def _usage_snapshot(plan: Plan) -> dict[str, Any]:
        return {
            "users": {
                "limit": plan.max_users,
                "used": 0,
            },
            "branches": {
                "limit": plan.max_branches,
                "used": 0,
            },
            "doctors": {
                "limit": plan.max_doctors,
                "used": 0,
            },
            "patients": {
                "limit": plan.max_patients,
                "used": 0,
            },
            "lab_orders": {
                "limit": plan.max_lab_orders,
                "used": 0,
            },
            "imaging_orders": {
                "limit": plan.max_imaging_orders,
                "used": 0,
            },
            "pharmacy_products": {
                "limit": plan.max_pharmacy_products,
                "used": 0,
            },
            "inventory_transactions": {
                "limit": plan.max_inventory_transactions,
                "used": 0,
            },
            "storage_gb": {
                "limit": plan.max_storage_gb,
                "used": 0,
            },
            "api_requests": {
                "limit": plan.max_api_requests,
                "used": 0,
            },
            "ai_requests": {
                "limit": plan.max_ai_requests,
                "used": 0,
            },
            "ai_tokens": {
                "limit": plan.max_ai_tokens,
                "used": 0,
            },
        }

    @classmethod
    @transaction.atomic
    def provision(
        cls,
        *,
        tenant,
        organization,
        category: str,
        organization_type: str,
        size: str,
        tier: str,
        auto_renew: bool = True,
        start_immediately: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> Subscription:
        """
        Provision a subscription for an organization.

        Idempotency rule:

            One organization -> one subscription.

        The existing Subscription.organization OneToOneField is
        therefore treated as the authoritative uniqueness boundary.
        """

        existing = (
            Subscription.objects.select_related("plan")
            .filter(organization=organization)
            .first()
        )

        if existing is not None:
            raise SubscriptionAlreadyExistsError(
                f"The organization already has a subscription: {existing.pk}"
            )

        plan = cls.resolve_plan(
            category=category,
            organization_type=organization_type,
            size=size,
            tier=tier,
        )

        now = timezone.now()

        trial_days = int(plan.trial_days or 0)

        if trial_days > 0:
            status = Subscription.Status.TRIAL

            trial_start = now
            trial_end = now + timedelta(days=trial_days)

            current_period_start = now
            current_period_end = trial_end

            expires_at = trial_end

        elif start_immediately:
            status = Subscription.Status.ACTIVE

            trial_start = None
            trial_end = None

            current_period_start = now

            current_period_end = cls._calculate_period_end(
                now,
                plan.billing_cycle,
            )

            expires_at = current_period_end

        else:
            status = Subscription.Status.TRIAL

            trial_start = now
            trial_end = None

            current_period_start = None
            current_period_end = None
            expires_at = None

        subscription = Subscription.objects.create(
            tenant=tenant,
            organization=organization,
            plan=plan,
            status=status,
            trial_start=trial_start,
            trial_end=trial_end,
            started_at=now if start_immediately else None,
            current_period_start=current_period_start,
            current_period_end=current_period_end,
            expires_at=expires_at,
            auto_renew=auto_renew,
            plan_snapshot=cls._plan_snapshot(plan),
            feature_snapshot=cls._feature_snapshot(plan),
            seats_used=0,
            usage_snapshot=cls._usage_snapshot(plan),
            metadata={
                "provisioning": {
                    "category": category,
                    "organization_type": organization_type,
                    "size": size,
                    "tier": tier,
                },
                **(metadata or {}),
            },
        )

        return subscription

    @staticmethod
    def _calculate_period_end(
        start,
        billing_cycle: str,
    ):
        """
        Calculate a safe initial billing period.

        Month/year arithmetic is intentionally handled without
        introducing another dependency.
        """

        from calendar import monthrange

        cycle = str(billing_cycle or "MONTHLY").strip().upper()

        if cycle in {"YEARLY", "ANNUAL", "ANNUALLY"}:
            year = start.year + 1

            try:
                return start.replace(
                    year=year,
                )
            except ValueError:
                return start.replace(
                    year=year,
                    month=2,
                    day=28,
                )

        # Default to monthly.
        month = start.month + 1
        year = start.year

        if month == 13:
            month = 1
            year += 1

        day = min(
            start.day,
            monthrange(year, month)[1],
        )

        return start.replace(
            year=year,
            month=month,
            day=day,
        )


__all__ = [
    "PlanResolutionError",
    "SubscriptionAlreadyExistsError",
    "SubscriptionProvisioningError",
    "SubscriptionProvisioningService",
]

"""
Billing service.

Business logic layer for DatavionOS SaaS billing.

Responsibilities:

- Create billing accounts
- Update billing profiles
- Manage billing lifecycle
- Configure payment providers
- Manage auto charge
- Resolve billing capabilities

Architecture:

Organization
      |
BillingService
      |
Billing Workflow
      |
Billing Account
      |
Subscription
      |
Invoice
      |
Payment
      |
Revenue Analytics
"""

from __future__ import annotations

from django.db import transaction

from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.saas_billing.models import (
    BillingAccount,
)


class BillingService:
    """
    Enterprise SaaS billing service.
    """

    # ==============================================================
    # Queries
    # ==============================================================

    @staticmethod
    def get_billing_account(
        *,
        organization: Organization,
    ) -> BillingAccount | None:
        """
        Return organization billing account.
        """

        return BillingAccount.objects.filter(
            organization=organization,
        ).first()

    @staticmethod
    def is_active(
        *,
        billing_account: BillingAccount,
    ) -> bool:
        """
        Check billing account status.
        """

        return billing_account.status == BillingAccount.BillingStatus.ACTIVE

    @staticmethod
    def can_charge(
        *,
        billing_account: BillingAccount,
    ) -> bool:
        """
        Check whether account supports charging.
        """

        return (
            BillingService.is_active(
                billing_account=billing_account,
            )
            and billing_account.auto_charge_enabled
        )

    @staticmethod
    def get_payment_configuration(
        *,
        billing_account: BillingAccount,
    ) -> dict:
        """
        Resolve payment gateway configuration.
        """

        return {
            "provider": (billing_account.payment_provider),
            "customer_id": (billing_account.payment_customer_id),
            "payment_method_id": (billing_account.default_payment_method_id),
            "auto_charge": (billing_account.auto_charge_enabled),
        }

    # ==============================================================
    # Creation
    # ==============================================================

    @staticmethod
    @transaction.atomic
    def create_billing_account(
        *,
        organization: Organization,
        legal_name: str | None = None,
        billing_email: str | None = None,
        billing_phone: str = "",
        currency: str = "INR",
    ) -> BillingAccount:
        """
        Create organization billing account.

        Used during:

        - Organization signup
        - Tenant provisioning
        - SaaS onboarding
        """

        existing = BillingService.get_billing_account(
            organization=organization,
        )

        if existing:
            return existing

        return BillingAccount.objects.create(
            tenant=organization.tenant,
            organization=organization,
            legal_name=(legal_name or organization.name),
            billing_email=(billing_email or organization.email),
            billing_phone=billing_phone,
            currency=currency,
            status=(BillingAccount.BillingStatus.ACTIVE),
            metadata={
                "created_by": "organization_signup",
            },
        )

    # ==============================================================
    # Profile
    # ==============================================================

    @staticmethod
    @transaction.atomic
    def update_billing_profile(
        *,
        billing_account: BillingAccount,
        data: dict,
    ) -> BillingAccount:
        """
        Update billing information.
        """

        allowed_fields = {
            "legal_name",
            "billing_email",
            "billing_phone",
            "billing_contact_name",
            "gst_number",
            "vat_number",
            "tax_id",
            "billing_address",
            "tax_configuration",
            "payment_terms",
        }

        updated_fields = []

        for field, value in data.items():
            if field in allowed_fields:
                setattr(
                    billing_account,
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

            billing_account.save(
                update_fields=updated_fields,
            )

        return billing_account

    # ==============================================================
    # Payment Provider
    # ==============================================================

    @staticmethod
    @transaction.atomic
    def configure_payment_provider(
        *,
        billing_account: BillingAccount,
        provider: str,
        customer_id: str | None = None,
        payment_method_id: str | None = None,
    ) -> BillingAccount:
        """
        Configure external payment provider.
        """

        billing_account.payment_provider = provider

        if customer_id is not None:
            billing_account.payment_customer_id = customer_id

        if payment_method_id is not None:
            billing_account.default_payment_method_id = payment_method_id

        billing_account.save(
            update_fields=[
                "payment_provider",
                "payment_customer_id",
                "default_payment_method_id",
                "updated_at",
            ],
        )

        return billing_account

    # ==============================================================
    # Auto Charge
    # ==============================================================

    @staticmethod
    @transaction.atomic
    def enable_auto_charge(
        *,
        billing_account: BillingAccount,
    ) -> BillingAccount:

        billing_account.auto_charge_enabled = True

        billing_account.save(
            update_fields=[
                "auto_charge_enabled",
                "updated_at",
            ],
        )

        return billing_account

    @staticmethod
    @transaction.atomic
    def disable_auto_charge(
        *,
        billing_account: BillingAccount,
    ) -> BillingAccount:

        billing_account.auto_charge_enabled = False

        billing_account.save(
            update_fields=[
                "auto_charge_enabled",
                "updated_at",
            ],
        )

        return billing_account

    # ==============================================================
    # Lifecycle
    # ==============================================================

    @staticmethod
    @transaction.atomic
    def suspend(
        *,
        billing_account: BillingAccount,
    ) -> BillingAccount:

        billing_account.status = BillingAccount.BillingStatus.SUSPENDED

        billing_account.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return billing_account

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        billing_account: BillingAccount,
    ) -> BillingAccount:

        billing_account.status = BillingAccount.BillingStatus.ACTIVE

        billing_account.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return billing_account

    @staticmethod
    @transaction.atomic
    def close(
        *,
        billing_account: BillingAccount,
    ) -> BillingAccount:

        billing_account.status = BillingAccount.BillingStatus.CLOSED

        billing_account.auto_charge_enabled = False

        billing_account.save(
            update_fields=[
                "status",
                "auto_charge_enabled",
                "updated_at",
            ],
        )

        return billing_account


# Backward compatibility alias.
#
# Existing workflows and services may import
# BillingAccountService.
#
# BillingService is the canonical implementation.

BillingAccountService = BillingService


__all__ = [
    "BillingService",
    "BillingAccountService",
]

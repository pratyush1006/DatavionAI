"""
Billing account services.

Business logic layer for DatavionOS SaaS billing accounts.

Responsibilities:

- Create billing accounts
- Update billing profiles
- Manage billing lifecycle
- Configure payment providers
- Enterprise billing settings

Architecture:

Organization
      |
BillingAccountService
      |
Billing Workflow
      |
BillingAccount Model
      |
Subscription
      |
Invoice
      |
Payment
"""

from __future__ import annotations

from django.db import transaction

from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.saas_billing.models import (
    BillingAccount,
)


class BillingAccountService:
    """
    Enterprise SaaS billing account service.
    """

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
        Create billing account.

        Used during:

        - Organization registration
        - SaaS onboarding
        - Tenant provisioning
        """

        existing = BillingAccountService.get_billing_account(
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
                "created_by": ("organization_signup"),
            },
        )

    @staticmethod
    @transaction.atomic
    def update_billing_profile(
        *,
        billing_account: BillingAccount,
        data: dict,
    ) -> BillingAccount:
        """
        Update billing profile.
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

    @staticmethod
    @transaction.atomic
    def enable_auto_charge(
        *,
        billing_account: BillingAccount,
    ) -> BillingAccount:
        """
        Enable automatic payment collection.
        """

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
        """
        Disable automatic payment collection.
        """

        billing_account.auto_charge_enabled = False

        billing_account.save(
            update_fields=[
                "auto_charge_enabled",
                "updated_at",
            ],
        )

        return billing_account

    @staticmethod
    @transaction.atomic
    def suspend(
        *,
        billing_account: BillingAccount,
    ) -> BillingAccount:
        """
        Suspend billing account.
        """

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
        """
        Activate billing account.
        """

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
        """
        Close billing account.

        Also disables automatic collection.
        """

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


__all__ = [
    "BillingAccountService",
]
